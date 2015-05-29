import os
import sys
import json
import unittest

try:
    from hiparser import hiparser
except ImportError:
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from hiparser import hiparser


class HiparserTests(unittest.TestCase):
    def test_basic_mention(self):
        expected_result = {
            'mentions': ['blakfeld']
        }
        self.assertEqual(json.dumps(expected_result),
                         hiparser("Hey @blakfeld, what's crackin'?"))

    def test_basic_emoticon(self):
        expected_result = {
            'emoticons': ['lulwat']
        }
        self.assertEqual(json.dumps(expected_result),
                         hiparser("Wait, you want me to do what? (lulwat)"))

    def test_basic_url(self):
        expected_result = {
            'links': [{'url': 'http://google.com', 'title': 'Google'}]
        }
        self.assertEqual(json.dumps(expected_result),
                         hiparser("Dude, have you heard of http://google.com?"))

    def test_multiple_mentions(self):
        expected_result = {
            'mentions': ['sneezy',
                         'bashful',
                         'dopey',
                         'sleepy',
                         'happy',
                         'doc',
                         'grumpy']
        }
        self.assertItemsEqual(json.dumps(expected_result),
                              hiparser("All 7 dwarves are: "
                                    "@sneezy, @bashful, @dopey, @sleepy, "
                                    "@happy, @doc, @grumpy."))

    def test_multiple_emoticons(self):
        expected_result = {
            'emoticons': ['carl', 'sleep', 'dance']
        }
        self.assertEqual(json.dumps(expected_result),
                         hiparser("Hey (carl), don't (sleep)! We have to "
                               "(dance)!"))

    def test_multiple_urls(self):
        expected_result = {
            'links': [{'url': 'http://google.com', 'title': 'Google'},
                      {'url': 'https://yahoo.com', 'title': 'Yahoo'}]
        }
        self.assertEqual(json.dumps(expected_result),
                         hiparser("Ever since http://google.com "
                               " came out do people still go "
                               "to https://yahoo.com?"))

    def test_return_nothing(self):
        expected_result = {}
        self.assertEqual(json.dumps(expected_result),
                         hiparser('Theres nothing here to parse!'))

    def test_email_mention(self):
        expected_result = {}
        self.assertEqual(json.dumps(expected_result),
                         hiparser('Shoot me an e-mail at bill@domainname.tld'))

    def test_false_emoticon(self):
        expected_result = {}
        self.assertEqual(json.dumps(expected_result),
                         hiparser("What was that song? "
                               "Cowboy (Wanted dead or alive)?"))

    def test_better_false_emoticon(self):
        expected_result = {}
        self.assertEqual(json.dumps(expected_result),
                         hiparser("What was that song? "
                               "Cowboy (Wanteddeadoralive)?"))

    def test_false_url(self):
        expected_result = {}
        self.assertEqual(json.dumps(expected_result),
                         hiparser("Why don't you go to "
                               "http://pleasegoawayIhoptthisisnotasite.test"))

    def test_hidden_mention(self):
        expected_result = { 'mentions': ['john']}
        self.assertEqual(json.dumps(expected_result),
                         hiparser('hey @john1234123.'))
