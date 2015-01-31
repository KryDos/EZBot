"""
thanks.py
Copyright 2015, http://evilzone.org

Licensed under the Evilzone Forum License.
EZbot: https://evilzone.org
"""

import random
from willie.module import commands, example
from willie.tools import Identifier

@commands('insult')
@example('.insult kenjoe41')
def insult(bot, trigger): 
   if not trigger.group(2):
      return bot.say(".insult <nick> - Insults the user.")
   
   _insult = random.choice((
     'Shut up',
     'I hate you',
     'Go away',
     'Eat a boat',
     'Leave me alone',
     'Get bent',
     'Screw you',
     'Nopony loves you',
     'Get out',
     'Go swivel',
     'I\'ve had my genitals on live television, I don\'t need your crap',
     'You\'re not my real mom',
     'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
   ))
   insultednick = Identifier(trigger.group(2).strip())
   bot.say(_insult +  ", " + insultednick + "!")
if __name__ == '__main__': 
   print(__doc__.strip())
