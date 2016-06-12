Terribot
========
A terrible Telegram chat robot.

# Using it
This is a Python project, so if you're familiar with the language, you're ready to go. It depends on the [tg](https://github.com/vysheng/tg) [Telegram](https://telegram.org/) client, so you'll need that installed as well. tg should be run using the `--json -P 4458` argument. This will allow Terribot to communicate with the client.

## First-time setup
The first thing you'll need is to set up the Telegram CLI client. You can do this by running:

```docker run -it -v $HOME/.telegram-cli:/home/telegram/.telegram-cli justingood/tg```

It will prompt you for your account details, and will set up an account for you. The resulting configuration will be saved in `$HOME/.telegram-cli`

## Docker
This currently runs with [Docker](https://www.docker.com/what-docker). There is a [docker-compose](https://docs.docker.com/compose/) file that can get the Telegram client and the bot up and running quickly:

```docker-compose up```

# Developing
If you want to work on the bot the plugins are probably what you'll want to deal with. Should be fairly straightforward.

## Plugins
Generally, this is probably what you'll want to edit. Each of the plugins in the **plugin** directory performs a function in response to a trigger phrase.

### Anatomy of a Plugin
When the program starts, it will automatically load the `.py` files in the **plugin** subdirectory, and record the attributes of each in a [TinyDB](https://github.com/msiemens/tinydb) database. The plugin must define certain attributes to be loaded correctly.

As an example:
```
def setup():
    return {'regex': "^test.*", 'act_on_event': 'message', 'cooldown': 10}

def run(msg):
    return ({'action': 'send_msg', 'payload': "test received"},)
```
* **setup()**
 * This function defines the plugin attributes. It's activated when the program starts and loads all the plugins.
 * It's expressed as a [dictionary](https://docs.python.org/3.5/tutorial/datastructures.html#dictionaries) of the attributes.
 * Return Attributes (The values that get passed back to the bot):
    * **regex**: The [regular expression](https://docs.python.org/3/library/re.html) that must be matched to activate the plugin.
    * **act_on_event**: What type of Telegram incoming event this plugin should act upon. Currently, only text messages are supported, but this could be extended to act on other types fairly easily.
    * **cooldown**: Every plugin is subject to a cooldown period to ensure a function is not spammed. If the default (_60s_) is too short or too long, then you can override the value here.

* **run(msg)**
  * This function runs when the plugin is triggered, and is passed the full _msg_ from Telegram.
  * The return value is what is sent back to the bot to pass onto the user/group.
  * The return is provided as a [tuple](https://docs.python.org/3.5/tutorial/datastructures.html#tuples-and-sequences). Each message is one element in the tuple. This allows us to send more than one message in response, if we wish. When sending a single message response, make sure to include the trailing comma, to indicate that it is a single-element tuple.
  * Return Attributes
      * **action**: What the response should do. Currently, you are able to send a message, or a photo.
      * **payload**: The actual response data. Usually this will be either text, or the path to an image.

  ## Getting Your Changes Into the Bot
  [Fork](https://help.github.com/articles/fork-a-repo/) the repository to your own account and make your changes locally. Test them by running the bot locally. Then, send a [pull request](https://help.github.com/articles/creating-a-pull-request/) to get your changes merged and deployed.

## Testing
Docker compose works pretty well for testing changes:

```docker-compose up --build```
