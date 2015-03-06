# -*- coding: utf8 -*-
"""
love.py  EZbot love module
Copyright 2015, http://evilzone.org

Licensed under the Evilzone Forum License.
EZbot: https://evilzone.org
"""

from willie.module import commands, example
from willie.tools import Identifier
import random

@commands('love')
@example('.love kenjoe41')
def love(bot, trigger):
	"""Shows some love to the specified nick."""
	if not trigger.group(2):
        	bot.say(".love <nick> - Shows some love to the specified nick.")
        	return
	lovednick = Identifier(trigger.group(2).strip())
	bot.action(' goes to %s %s %s' %(randomlove(), lovednick, randomplace()))

def randomlove():
	loves = ['love', 'cuddle with', 'hug', 'kiss', 'anal-examine', 'squirt allover']
	return random.choice(loves)

def randomplace():
	places = ['on the table.', 'in the corner.', 'up in the tree.', 'under the bed.']
	return random.choice(places)

if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)#add test data for this module.
