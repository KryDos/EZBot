# -*- coding: utf8 -*-
"""
howdoi.py  EZbot howdoi module
Copyright (C) 2012 Benjamin Gleitzman (gleitz@mit.edu)
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.

Copyright 2015, http://evilzone.org
EZbot: https://evilzone.org
"""
import argparse
import glob
import os
import random
import re
import requests
import requests_cache
import sys

try:
    from urllib.parse import quote as url_quote
except ImportError:
    from urllib import quote as url_quote

try:
    from urllib import getproxies
except ImportError:
    from urllib.request import getproxies

from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError

__version__ = '1.1.7'


from willie.module import commands, example

# Handle unicode between Python 2 and 3
# http://stackoverflow.com/a/6633040/305414
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


if os.getenv('HOWDOI_DISABLE_SSL'):  # Set http instead of https
    SEARCH_URL = 'http://www.google.com/search?q=site:{0}%20{1}'
else:
    SEARCH_URL = 'https://www.google.com/search?q=site:{0}%20{1}'

URL = os.getenv('HOWDOI_URL') or 'stackoverflow.com'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)
ANSWER_HEADER = u('--- Answer {0} ---\n{1}')
NO_ANSWER_MSG = '< no answer given >'
XDG_CACHE_DIR = os.environ.get('XDG_CACHE_HOME',
                               os.path.join(os.path.expanduser('~'), '.cache'))
CACHE_DIR = os.path.join(XDG_CACHE_DIR, 'howdoi')
CACHE_FILE = os.path.join(CACHE_DIR, 'cache{0}'.format(
        sys.version_info[0] if sys.version_info[0] == 3 else ''))



@commands('howdoi')
@example('.howdoi google myself')
def howdoi(bot, trigger):
	"""Search easily for programming questions without
		firing up you browser."""
	if not trigger.group(2):
        	return bot.say(".howdoi <query> - Searches for query on stackoverflow.")
	try:
		query = trigger.group(2)
		query_response, uri = hdi(query)
		bot.reply(uri)
	except Exception:
		bot.say('[!]Something went wrong. Try again later!')
	#TODO: Use EZbot's built in memory to cache queries.


def hdi(query):
    query = ' '.join(query).replace('?', '')
    try:
        return get_instructions(query) or 'Sorry, couldn\'t find any help with that topic\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'

def get_proxies():
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = 'http://%s' % value
            else:
                filtered_proxies[key] = value
    return filtered_proxies


def get_result(url):
    try:
        return requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}, proxies=get_proxies()).text
    except requests.exceptions.SSLError as e:
        print('[ERROR] Encountered an SSL Error. Try using HTTP instead of '
              'HTTPS by setting the environment variable "HOWDOI_DISABLE_SSL".\n')
        raise e


def is_question(link):
    return re.search('questions/\d+/', link)


def get_links(query):
    result = get_result(SEARCH_URL.format(URL, url_quote(query)))
    html = pq(result)
    return [a.attrib['href'] for a in html('.l')] or \
        [a.attrib['href'] for a in html('.r')('a')]


def get_link_at_pos(links, position):
    links = [link for link in links if is_question(link)]
    if not links:
        return

    if len(links) >= position:
        link = links[position-1]
    else:
        link = links[-1]
    return link


def get_answer(links):
    link = get_link_at_pos(links, 1)
    if not link:
        return False
    page = get_result(link + '?answertab=votes')
    html = pq(page)

    first_answer = html('.answer').eq(0)
    instructions = first_answer.find('pre') or first_answer.find('code')

    if not instructions:
        text = first_answer.find('.post-text').eq(0).text()
    else:
        text = instructions.eq(0).text()
    if text is None:
        text = NO_ANSWER_MSG
    text = text.strip()
    return text


def get_instructions(query):
    links = get_links(query)

    if not links:
        return 'Sorry, nothing founder. Google some more.'

    answer = get_answer(links[1])

    return answer, links[1]


