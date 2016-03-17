import time
import re
import random
import logging
import urllib2
import json
import urllib
crontable = []
outputs = []
attachments = []
typing_sleep = 0

googleapikey = None

greetings = ['Hi friend!', 'Hello there.', 'Howdy!', 'Wazzzup!!!', 'Hi!', 'Hey.']
help_text = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
    "I will respond to the following messages: ",
    "`chimbot hi` for a random greeting.",
    "`chimbot joke` for a question, typing indicator, then answer style joke.",
    "`chimbot attachment` to see a Slack attachment message.",
    "`@<your bot's name>` to demonstrate detecting a mention.",
    "`chimbot image me <something>` to pop up a random image for your query.",
    "`chimbot call the soul` to get a random CtS draw.",
    "`chimbot roll me xdxx to get a random dice roll.",
    "`chimbot help` to see this again.")

# regular expression patterns for string matching
p_bot_hi = re.compile("chimbot[\s]*hi", re.I)
p_bot_joke = re.compile("chimbot[\s]*joke", re.I)
p_bot_attach = re.compile("chimbot[\s]*attachment", re.I)
p_bot_help = re.compile("chimbot[\s]*help", re.I)
p_bot_image = re.compile("chimbot[\s]*image[\s]*me", re.I)
p_bot_key = re.compile("chimbot[\s]*google[\s]*API[\s]*key", re.I)
p_bot_cts = re.compile("chimbot[\s]*call[\s]*the[\s]*soul", re.I)
p_bot_cthulhu = re.compile("chimbot[\s]*summon[\s]*cthulhu", re.I)
p_bot_die = re.compile("chimbot[\s]*roll[\s]*me", re.I)

def process_message(data):
    logging.debug("process_message:data: {}".format(data))

    if p_bot_hi.match(data['text']):
        outputs.append([data['channel'], "{}".format(random.choice(greetings))])
    
    elif p_bot_key.match(data['text']):
    	global googleapikey
    	googleapikey = str(data['text'])
 	googleapikey = re.sub("C(?i)himbot[\s]*google[\s]*API[\s]*key[\s]*", '', googleapikey)
 	outputs.append([data['channel'], "You input: " + googleapikey])

    elif p_bot_cthulhu.match(data['text']):
    	resist = random.randint(0,1)
    	if resist == 0:
    		outputs.append([data['channel'], "Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn."])
    		outputs.append([data['channel'], "__typing__", 1])
    		outputs.append([data['channel'], "Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn."])
    		outputs.append([data['channel'], "__typing__", 1])
    		outputs.append([data['channel'], "Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn."])
    		outputs.append([data['channel'], "__typing__", 1])
    		outputs.append([data['channel'], ":cthulhu: CTHULHU AWAKENS! :cthulhu:"])
    	else:
    		outputs.append([data['channel'], "Resist Magic!"])
    
    elif p_bot_joke.match(data['text']):
        outputs.append([data['channel'], "Why did the python cross the road?"])
        outputs.append([data['channel'], "__typing__", 5])
        outputs.append([data['channel'], "To eat the chicken on the other side! :laughing:"])

    elif p_bot_attach.match(data['text']):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachments.append([data['channel'], txt, build_demo_attachment(txt)])

    elif p_bot_help.match(data['text']):
        outputs.append([data['channel'], "{}".format(help_text)])
        
    elif p_bot_cts.match(data['text']):
    	cts = random.randint(0,4)
    	if cts > 0:
    		outputs.append([data['channel'], "White stone, success!"])
    	else:
    		outputs.append([data['channel'], "Black stone, failure!"])
    
    elif p_bot_die.match(data['text']):
    	numdie = 1
    	dietype = -1
    	rollinfo = str(data['text'])
    	rollinfo = re.sub("C(?i)himbot[\s]*roll[\s]*me[\s]*", '', rollinfo)
    	if re.match(r"\d*d(?i)(\d*|f(?i)udge$)", rollinfo):
    		numdie = re.sub("d(?i)(\d\d\d|\d\d|\d|f(?i)udge)", '', rollinfo)
    		dietype = re.sub("(\d|\d\d|\d\d\d)d(?i)", '', rollinfo)
    		if re.match("(\d|\d\d|\d\d\d)d(?i)f(?i)udge", rollinfo):
    			outputs.append([data['channel'], "This Functionality Coming Soon"])
    	
    		else:
    			result = 0
    			numdie = int(numdie)
    			dietype = int(dietype)
    			for x in range (numdie):
    				result += random.randint(1, dietype)
    			outputs.append([data['channel'], str(result)])
    	else:
    		outputs.append([data['channel'], "Invalid"])
    	
    
    elif p_bot_image.match(data['text']):
    	global googleapikey
 	image = str(data['text'])
 	image = re.sub("C(?i)himbot[\s]*image[\s]*me[\s]*", '', image)
 	fetcher = urllib2.build_opener()
	startIndex = str("0")
	searchUrl = "https://www.googleapis.com/customsearch/v1?" + urllib.urlencode([("key", googleapikey), ("cx", "009488714636722478744:yz25mu3sy4y"), ("q", image), ("count", "1"), ("searchType", "image")])
	f = None
	try:
		rand = random.randint(0,9)
		f = fetcher.open(searchUrl)
		deserialized_output = json.load(f)
		links = str(deserialized_output['items'][rand]['link'])
		outputs.append([data['channel'], links])
		
	except urllib2.URLError as e:
		e = str(e)
    		outputs.append([data['channel'], e])
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
