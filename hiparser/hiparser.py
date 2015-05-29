"""
hiparser.py -- Code to handle parsing special commands out of a string,
    then return them as JSON.

Author: Corwin Brown
E-Mail: corwin@corwinbrown.com
Date: 5/27/2015
"""

import re
import sys
import json
import urllib2
from string import punctuation
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup


def parse_mentions(input_str):
    """
    Parse '@mentions' out of a string, perform any formatting/munging
        and return a list of all we found.

    Args:
        input_str (str):    The string to parse.

    Returns:
        list:               List of all mentioned users.
    """

    # Seems reasonable to assume the mention will always happen at
    #   the beginning of the string, or have a space before.
    mention_re = re.compile(r'(\s@[a-zA-Z]+|^@[a-zA-Z]+)')

    mentions = mention_re.findall(input_str)

    return [m.replace('@', '').strip() for m in mentions]


def parse_emoticons(input_str):
    """
    Parse '(emoticons)' out of a string, perform any formatting/munging
        and return a list of all we found.

    Args:
        input_str (str):    The string to parse.

    Returns:
        list:               List of all found emoticons.
    """

    emoticon_re = re.compile(r'\([a-zA-Z\d]{1,15}\)')

    emoticons = emoticon_re.findall(input_str)

    return [re.sub(r'(\(|\))', '', e) for e in emoticons]


def parse_url(input_str):
    """
    Parse urls out of a string, perform any formatting/munging, gather
        the title of the site the URL refers to, and return a list
        of dicts containing the link, and the page title.

    Args:
        input_str (str):    The string to parse.

    Returns:
        list:               list of dicts with the following keys:
                                - url
                                - title
    """

    # URL regexes are insane. So I'm going to find something that *looks*
    #   like it might be a url, then have urlparse validate it. Although
    #   of course it's ultimate validation will be attempting to retrieve
    #   the title.
    url_re = re.compile(r'(https?:\/\/\S+)')

    urls = url_re.findall(input_str)

    result = []
    for url in urls:
        # If the URL ends in any punctuation, lets cut it off.
        #   this could be bad, but I can't think of a case where it would
        #   hose me unless something was real dumb.
        if url[-1] in punctuation:
            url = url[:-1]

        if not urlparse(url).netloc:
            # This will only be None/False/blank if the URL is invalid.
            continue

        try:
            r = urllib2.urlopen(url)
            content = r.read()
        except urllib2.HTTPError:
            content = ''
        except urllib2.URLError:
            # If we can't even talk to the server, lets punt and say this is
            #   an invalid URL.
            continue

        soup = BeautifulSoup(content,
                             convertEntities=BeautifulSoup.HTML_ENTITIES)
        title = soup.find('title')

        try:
            title = title.renderContents()
        except AttributeError:
            title = ''

        result.append({
            'url': url,
            'title': title
        })

    return result


def output_json(data):
    """
    Utility function to dump 'data' out to json. Any key's that have a
        "Falsy" value will be ignored.

    Args:
        data (dict):        The dictionary we want to serialize out to JSON.
        json_indent (int):  Pretty print JSON.

    Returns:
        json:               The serialized dictionary.
    """

    output = {}
    for k, v, in data.items():
        if v:
            output[k] = v

    return json.dumps(output)


def hiparser(input_str):
    """
    Take in a String, and parse out '@mentions', '(emoticons)', and
        urls, and output them as JSON.

    Example:

        Input:
            "@bob (sadface) did you see this! http://sadnewssite.com"

        Output:
            {
                "mentions": [
                    "bob"
                ],
                "emoticons": [
                    "success"
                ],
                "links": [
                    {
                        "url": "http://sadnewssite.com",
                        "title": "Super sad news today!".
                    }
                ]
            }

    Args:
        input_str (str):    The string to parse/munge.

    Returns:
        dict:               A dictionary representation of the data
                                structure noted above.
    """

    result = {}

    result['mentions'] = parse_mentions(input_str)
    result['emoticons'] = parse_emoticons(input_str)
    result['links'] = parse_url(input_str)

    return output_json(result)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('Please write some text to feed to the parser')
        sys.exit(1)

    user_input = ' '.join(sys.argv[1:])

    print('{}'.format(hiparser(user_input)))
    sys.exit(0)
