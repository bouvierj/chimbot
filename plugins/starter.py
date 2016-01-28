import time
import re
import random
import logging
import urllib2
import simplejson
crontable = []
outputs = []
attachments = []
typing_sleep = 0

greetings = ['Hi friend!', 'Hello there.', 'Howdy!', 'Wazzzup!!!', 'Hi!', 'Hey.']
help_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
    "I will respond to the following messages: ",
    "`chimbot hi` for a random greeting.",
    "`chimbot joke` for a question, typing indicator, then answer style joke.",
    "`chimbot attachment` to see a Slack attachment message.",
    "`@<your bot's name>` to demonstrate detecting a mention.",
    "`chimbot help` to see this again.")

# regular expression patterns for string matching
p_bot_hi = re.compile("chimbot[\s]*hi")
p_bot_joke = re.compile("chimbot[\s]*joke")
p_bot_attach = re.compile("chimbot[\s]*attachment")
p_bot_help = re.compile("chimbot[\s]*help")
p_bot_image = re.compile("chimbot[\s]*image[\s]*me")

def process_message(data):
    logging.debug("process_message:data: {}".format(data))

    if p_bot_hi.match(data['text']):
        outputs.append([data['channel'], "{}".format(random.choice(greetings))])

    elif p_bot_joke.match(data['text']):
        outputs.append([data['channel'], "Why did the python cross the road?"])
        outputs.append([data['channel'], "__typing__", 5])
        outputs.append([data['channel'], "To eat the chicken on the other side! :laughing:"])

    elif p_bot_attach.match(data['text']):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachments.append([data['channel'], txt, build_demo_attachment(txt)])

    elif p_bot_help.match(data['text']):
        outputs.append([data['channel'], "{}".format(help_text)])
    
    elif p_bot_image.match(data['text']):
 	image = str(data['text'])
 	image = re.sub("chimbot[\s]*image[\s]*me", '', image)
 	outputs.append([data['channel'], "This functionality is coming soon, you searched for: " + image])   
 	fetcher = urllib2.build_opener()
	startIndex = 0
	searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + image + "&start=" + startIndex
	f = fetcher.open(searchUrl)
	deserialized_output = simplejson.load(f)
	outputs.append([data['channel'], deserialized_output)
    
    elif data['text'].startswith("chimbot"):
        outputs.append([data['channel'], "I'm sorry, I don't know how to: `{}`".format(data['text'])])

    elif data['channel'].startswith("D"):  # direct message channel to the bot
        outputs.append([data['channel'], "Hello, I'm the chimbot.\n{}".format(help_text)])

def process_mention(data):
    logging.debug("process_mention:data: {}".format(data))
    outputs.append([data['channel'], "You really do care about me. :heart:"])

def build_demo_attachment(txt):
    return {
        "pretext" : "We bring bots to life. :sunglasses: :thumbsup:",
		"title" : "Host, deploy and share your bot in seconds.",
		"title_link" : "https://beepboophq.com/",
		"text" : txt,
		"fallback" : txt,
		"image_url" : "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
		"color" : "#7CD197",
    }
