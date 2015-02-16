"""
insult.py - insult nick using the Elizabethian system
Copyright 2015, http://evilzone.org

Licensed under the Evilzone Forum License.
EZbot: https://evilzone.org
"""

import random
from willie.module import commands, example
from willie.tools import Identifier

@commands('insult')
@example('!insult kenjoe41')
def insult(bot, trigger): 
	"""insult <nick> - insult nick using the Elizabethian system"""
	if not trigger.group(2):
		return bot.say("!insult <nick> - Insults the user.")
   
  	raw = web.get('http://quandyfactory.com/insult/json')
	insults = json.loads(raw)
	if trigger.group(2):
		insultednick = Identifier(trigger.group(2).strip())
		bot.say( insultednick + ', ' + insults['insult'])
	else:
		bot.say(trigger.nick + ', ' + insults['insult'])
if __name__ == '__main__': 
   print(__doc__.strip())
