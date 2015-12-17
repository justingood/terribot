import os
import time
import re
import loadplugins
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

# Plugin data is stored in TinyDB
plugindb = TinyDB(storage=MemoryStorage)
Plugins = Query()

# Load all of our plugins and populate our TinyDB with plugin settings.
loadplugins.do("plugins", globals(), plugindb)


class Terribot(object):
    """A terrible Telegram chat bot"""

    def __init__(self):
        receiver = Receiver(host='localhost', port=4458)
        sender = Sender(host='localhost', port=4458)
        receiver.start()
        receiver.message(self.listen(receiver, sender))
        print("Program exiting. Stopped at:", time.strftime("%Y/%m/%d-%H:%M:%S"))
        receiver.stop()

    @coroutine
    def listen(self, receiver, sender):
        print("Started, and waiting for messages at:", time.strftime("%Y/%m/%d %H:%M:%S"))
        try:
            while True:
                msg = (yield)
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
        # If the event type is message, we'll handle it.
        if msg['event'] == 'message':
            # if 'media' in msg and not msg['own']:
            #     # We don't handle media currently
            #     return None
            if 'text' in msg and not msg['own']:
                # These are standard messages
                response = self.callplugin(msg, event_type)
                return response

    def callplugin(self, msg, event_type):
        # Grab the list of plugins that can act on our event type
        pluginlist = plugindb.search(Plugins.act_on_event == event_type)
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
            plugindb.update({'last_execution': time.time()}, Plugins.name == plugin['name'])
            return True
        else:
            return False


if __name__ == '__main__':
    # Start the bot
    terribot = Terribot()
