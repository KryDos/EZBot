# -*- coding: utf8 -*-
"""
shoe.py - EZbot shoe module
Copyright 2015, http://evilzone.org

Licensed under the Evilzone Forum License.
EZbot: https://evilzone.org
"""

from willie.module import commands, example
from willie.tools import Identifier

@commands('shoe')
@example('.shoe kenjoe41')
def shoe(bot, trigger):
	"""Throws a shoe to specified user."""
	if not trigger.group(2):
	        bot.say(".shoe <nick> - Throws a shoe at a specified nick.")
        	return
	hitnick = Identifier(trigger.group(2).strip())
	bot.action(' hits %s with a shoe.' %hitnick)

if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)#add test data for this module.
