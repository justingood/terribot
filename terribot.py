import os
import sys
import socket
import signal
import time
import re
import json
import loadplugins
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

# Plugin data is stored in TinyDB
plugindb = TinyDB(storage=MemoryStorage)
plugins = Query()

# Load all of our plugins and populate our TinyDB with plugin settings.
loadplugins.do("plugins", globals(), plugindb)

# Figure out if we're in debug mode
try:
    debug = bool(os.environ['DEBUG'])
except:
    debug = False
    print('Debug flag not set - running in production mode')

class Terribot(object):
    """A terrible Telegram chat bot"""

    def __init__(self):
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        receiver = Receiver(host='tg', port=4458)
        sender = Sender(host='tg', port=4458)
        receiver.start()
        receiver.message(self.listen(receiver, sender))
        print("Program exiting. Stopped at:", time.strftime("%Y/%m/%d-%H:%M:%S"))
        receiver.stop()

    def sigterm_handler(self, signum, frame):
        print("Received stop signal. Shutting down.")
        sys.exit(0)

    @coroutine
    def listen(self, receiver, sender):
        print("Started, and waiting for messages at:", time.strftime("%Y/%m/%d %H:%M:%S"))
        try:
            while True:
                msg = (yield)
                print(msg)
                # uncomment for easier-to-read message chunks
                # print(json.dumps(msg, sort_keys=True, indent=4))
                action = self.process(msg)
                # If an action is necessary, we'll use the send method
                if action:
                    # Tell everyone ED is 'typing'
                    self.send_typing(sender, msg['peer']['cmd'])
                    # Send the result from the plugin
                    self.send(sender, msg['peer']['cmd'], action)
        except KeyboardInterrupt:
            print("Keyboard kill received. Exiting.")

    def process(self, msg):
        event_type = msg['event']
        # If it's a text message not from us, and directly to the bot while in debug mode we'll act on it.
        if msg['event'] == 'message' and 'text' in msg and not msg['own'] and debug is True and msg['peer']['type'] == 'user':
                # These are standard messages
                response = self.callplugin(msg, event_type)
                return response
        # If it's a text message and it's not from us, we'll act on it.
        elif msg['event'] == 'message' and 'text' in msg and not msg['own'] and debug is False:
                # These are standard messages
                response = self.callplugin(msg, event_type)
                return response

    def callplugin(self, msg, event_type):
        # Grab the list of plugins that can act on our event type
        pluginlist = plugindb.search(plugins.act_on_event == event_type)
        # Check if any of them match the regex
        for pluginname in pluginlist:
            if re.match(pluginname['regex'], msg['text'], re.IGNORECASE):
                # Make sure we're not being too ambitious
                if self.cooldown(pluginname):
                    # When it matches, call the run function in the plugin
                    function = globals()[pluginname['name']]
                    try:
                        pluginresult = getattr(function, 'run')(msg)
                    except:
                        print("Error with ", pluginname, ": ", pluginresult)
                    if pluginresult:
                        return pluginresult
                # If the cooldown period hasn't elapsed, we do not approve.
                else:
                    return ({'action': 'send_msg', 'payload': "ಠ_ಠ"},)
        return None

    def send(self, sender, send_to, senddata):
        # Unpack the tuples and process
        for index, message in enumerate(senddata):
            if message['action'] == 'send_msg':
                self.send_msg(sender, send_to, message['payload'])
            if message['action'] == 'send_photo':
                self.send_photo(sender, send_to, message['payload'])

    def send_msg(self, sender, send_to, payload):
        try:
            sender.msg(send_to, payload)
        except (NoResponse, ConnectionError) as e:   # NOQA
            print('Oops, had a connectivity problem while sending: ', send_to, payload, e)

    def send_photo(self, sender, send_to, filename):
        try:
            sender.send_file(send_to, filename)
        except (NoResponse, ConnectionError) as e:   # NOQA
            print('Oops, had a connectivity problem while sending: ', send_to, filename, e)
        time.sleep(0.2)
        os.remove(filename)

    def send_typing(self, sender, peer):
        sender.send_typing(peer)

    def cooldown(self, plugin):
        if time.time() - plugin['last_execution'] > plugin['cooldown']:
            plugindb.update({'last_execution': time.time()}, plugins.name == plugin['name'])
            return True
        else:
            return False


if __name__ == '__main__':
    # Wait for port to be responsive
    tg_ready = False

    while tg_ready is False:
      print("Trying to connect to Telegram-CLI...")
      try:
        s = socket.create_connection(('tg', 4458), 3)
        s.close()
        print("Telegram-CLI is ready for connections")
        tg_ready = True
      except socket.error:
        print("Telegram-CLI isn't ready for connections yet")
        time.sleep(2)
        tg_ready = False

    # Start the bot
    terribot = Terribot()
