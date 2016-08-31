""" Terribot, a terrible Telegram chat bot.  """
import os
import sys
import socket
import signal
import time
import re
import loadplugins
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
# Used to format the messages when debugging
# import json

# Plugin & cooldown data is stored in TinyDB
plugindb = TinyDB(storage=MemoryStorage)
plugins = Query()
cooldowndb = TinyDB(storage=MemoryStorage)
cooldowns = Query()

# Load all of our plugins and populate our TinyDB with plugin settings.
loadplugins.do("plugins", globals(), plugindb)

# Figure out if we're in production mode
try:
    location = str(os.environ['ENV'])
except KeyError:
    location = 'development'
    print('location not defined - setting development mode')


class Terribot(object):
    """A terrible Telegram chat bot"""

    def __init__(self):
        """ Create receiver and sender for communicating with PyTG. """
        signal.signal(signal.SIGTERM, self.sigterm_handler)
        receiver = Receiver(host='tg', port=4458)
        sender = Sender(host='tg', port=4458)
        receiver.start()
        receiver.message(self.listen(receiver, sender))
        print("Program exiting. Stopped at:", time.strftime("%Y/%m/%d-%H:%M:%S"))
        receiver.stop()

    @staticmethod
    def sigterm_handler(signum, frame):
        """ Shut down once SIGTERM received. """
        print("Received stop signal. Shutting down.")
        sys.exit(0)

    @coroutine
    def listen(self, receiver, sender):
        """ Listen for messages from PyTG and process them. """
        print("Started, and waiting for messages at:", time.strftime("%Y/%m/%d %H:%M:%S"))
        try:
            while True:
                msg = (yield)
                print(msg)
                # uncomment for easier-to-read messages
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
        """ XXX """
        event_type = msg['event']
        # Dev mode should only respond to messages directly to the bot
        # If it's a message, containing text, not from the bot, the mode is not production, and it's in a p2p chat, it should be acted on.
        if msg['event'] == 'message' and 'text' in msg and not msg['own'] and location != 'production' and msg['peer']['type'] == 'user':
            # These are standard messages
            response = self.callplugin(msg, event_type)
            return response
        # Production mode should only respond to chat messages. This might be changed at a a later time.
        # If it's a text message and it's not from us, we'll act on it.
        elif msg['event'] == 'message' and 'text' in msg and not msg['own'] and location == 'production' and msg['peer']['type'] == 'chat':
                # These are standard messages
                response = self.callplugin(msg, event_type)
                return response

    def callplugin(self, msg, event_type):
        """ XXX """
        # Grab the list of plugins that can act on our event type
        pluginlist = plugindb.search(plugins.act_on_event == event_type)
        # Check if any of them match the regex
        for pluginname in pluginlist:
            if re.match(pluginname['regex'], msg['text'], re.IGNORECASE):
                # Make sure we're not being too ambitious
                if self.cooldown(pluginname, msg['peer']['peer_id']):
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
        """ XXX """
        # Unpack the tuples and process
        for message in senddata:
            if message['action'] == 'send_msg':
                self.send_msg(sender, send_to, message['payload'])
            if message['action'] == 'send_photo':
                self.send_photo(sender, send_to, message['payload'])

    @staticmethod
    def send_msg(sender, send_to, payload):
        """ XXX """
        try:
            sender.msg(send_to, payload)
        except (NoResponse, ConnectionError) as e:   # NOQA
            print('Oops, had a connectivity problem while sending: ', send_to, payload, e)

    @staticmethod
    def send_photo(sender, send_to, filename):
        """ XXX """
        try:
            sender.send_file(send_to, filename)
        except (NoResponse, ConnectionError) as e:   # NOQA
            print('Oops, had a connectivity problem while sending: ', send_to, filename, e)
        time.sleep(0.2)
        os.remove(filename)

    @staticmethod
    def send_typing(sender, peer):
        """ XXX """
        sender.send_typing(peer)

    @staticmethod
    def cooldown(plugin, peer_id):
        """ XXX """
        # First, use a get() from TinyDB 'to see if a cooldown entry exists for the plugin in this channel(peer_id)
        #    It will helpfully return None if it does not exist
        cooldownrecord = cooldowndb.get((cooldowns.peer_id == peer_id) & (cooldowns.name == plugin['name']))

        # If the record exists
        if cooldownrecord:
            # If the cooldown has elapsed
            if time.time() - cooldownrecord['last_execution'] > plugin['cooldown']:
                # This plugin is safe to run - it's past the cooldown period. We're going to update() the record via the TinyDB 'eid' for next time.
                cooldowndb.update({'last_execution': time.time()}, eids=[cooldownrecord.eid])
                return True
            # Otherwise, the cooldown has NOT elapsed, so the plugin is not allowed to run.
            else:
                return False
        # If the record does not exist yet, we'll allow it to run, and create a cooldown record for next time.
        else:
            cooldowndb.insert({'name': plugin['name'],
                               'peer_id': peer_id,
                               'last_execution': time.time()})
            return True


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
