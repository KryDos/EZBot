import sqlite3 as dbapi
import os, string

from willie.module import commands, example, rate
from willie.tools import Identifier


def setup(bot):
	conn = bot.db.connect()
	c = conn.cursor()
	try:
		c.execute('SELECT * FROM Karma')
	except StandardError:
        	c.execute('CREATE TABLE IF NOT EXISTS Karma(Nick TEXT NOT NULL, PositiveKarma INTEGER NOT NULL, NegativeKarma INTEGER NOT NULL, TotalKarma INTEGER NOT NULL)')
        	conn.commit()
    	conn.close()


@commands('addpoint')
@example('.addpoint <nick>')
@rate(20)
def addpoint(bot, trigger):
	"""Adds karma points to given nick."""
	if not trigger.group(2):
        	bot.reply(".addpoint <nick> - Adds karma points to given nick.")
        	return
	nick = Identifier(trigger.group(2).strip().lower())
	channel = string.lower(str(Identifier(trigger.sender)))
	if (nick == Identifier(trigger.nick.lower())):
		bot.reply("Gotcha, %s. You can't karma yourself, sorry!" % nick)
		return
	if nick not in bot.privileges[channel]:
		bot.reply("Sorry, nick %s not in %s current users." % (nick, channel))
		return

	conn = bot.db.connect()
	c = conn.cursor()
	with conn:
		c.execute('SELECT PositiveKarma, NegativeKarma, TotalKarma FROM Karma WHERE Nick = "%s"' % nick)
		result = c.fetchone()
		if result is not None:#nick exists.
			poskarma = result[0]
			negkarma = result[1]
			totalkarma = result[2]
			poskarma = int(poskarma) + 1
			totalkarma = poskarma - negkarma
			c.execute('UPDATE Karma SET PositiveKarma = %d, TotalKarma = %d WHERE Nick = "%s"' %(poskarma, totalkarma, nick))
			conn.commit()
			bot.say('%s: +%d/-%d, %d' % (nick, poskarma, negkarma, totalkarma))
		else:
			c.execute('INSERT INTO Karma VALUES("%s", %d, %d, %d)' % (nick, 1, 0, 1))
			conn.commit()
			bot.say('%s: +%d/-%d, %d' % (nick, 1, 0, 1))
	conn.close()

@commands('negpoint')
@example('.negpoint <nick>')
@rate(20)
def negpoint(bot, trigger):
	"""Removes karma points to given nick."""
	if not trigger.group(2):
        	bot.say(".negpoint <nick> - Removes karma points to given nick.")
        	return
	nick = Identifier(trigger.group(2).strip().lower())
	channel = string.lower(str(Identifier(trigger.sender)))
	if (nick == Identifier(trigger.nick.lower())):
		bot.reply("You can't karma yourself, sorry!")
		return
	if nick not in bot.privileges[channel]:
		bot.reply("Sorry, nick %s not in %s current users." % (nick, channel))
		return


	conn = bot.db.connect()
	c = conn.cursor()
	with conn:
		c.execute('SELECT PositiveKarma, NegativeKarma, TotalKarma FROM Karma WHERE Nick = "%s"' % nick)
		result = c.fetchone()
		if result is not None:#nick exists.
			poskarma = result[0]
			negkarma = result[1]
			totalkarma = result[2]

			negkarma = int(negkarma) + 1
			totalkarma = poskarma - negkarma
			c.execute('UPDATE Karma SET NegativeKarma = %d, TotalKarma = %d WHERE Nick = "%s"' %(poskarma, totalkarma, nick))
			conn.commit()
			bot.say('%s: +%d/-%d, %d' % (nick, poskarma, negkarma, totalkarma))
		else:
			c.execute('INSERT INTO Karma VALUES("%s", %d, %d, %d)' % (nick, 0, 1, -1))
			conn.commit()
			bot.say('%s: +%d/-%d, %d' % (nick, 0, 1, -1))
	conn.close()

@commands('point')
@example('.point <nick>')
def point(bot, trigger):
	"""Show the amount of points."""
	if not trigger.group(2):
        	bot.reply(".point <nick> - Show karma points of given nick.")
        	return
	nick = Identifier(trigger.group(2).strip().lower())
	conn = bot.db.connect()
	c = conn.cursor()
	with conn:
		c.execute('SELECT PositiveKarma, NegativeKarma, TotalKarma FROM Karma WHERE Nick = "%s"' % nick)
		result = c.fetchone()
		if result is not None:
			poskarma = result[0]
			negkarma = result[1]
			totalkarma = result[2]
			bot.say('%s: +%d/-%d, %d' % (nick, poskarma, negkarma, totalkarma))
		else:
			bot.say('Sorry, no karma points found for %s. User not in database' % nick)
	conn.close()

@commands('reset')
@example('.reset <nick>')
def reset(bot, trigger):
	"""Resets the karma points of a user. Admin only command."""
	if not trigger.group(2) or not trigger.admin:
        	bot.reply(".reset <nick> - Reset karma points of given nick. Admin only command.")
        	return
	nick = Identifier(trigger.group(2).strip().lower())
	conn = bot.db.connect()
	c = conn.cursor()
	with conn:
		c.execute('SELECT PositiveKarma, NegativeKarma, TotalKarma FROM Karma WHERE Nick = "%s"' % nick)
		result = c.fetchone()
		if result is None:#nick doesn't exists.
			bot.say('User %s not found in the database. Reset not necessary.' % nick)
			return
		c.execute('DELETE FROM Karma WHERE nick = "%s"' % nick)
		conn.commit()
	conn.close()
	bot.say('Karma for account %s has successfully been reset.' % nick)
