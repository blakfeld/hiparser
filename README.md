# Hiparser (HipChat Parser)

A fun script to emulate parsing out commands from a chat client.

I went through a few variations on how I wanted to handle the parsing. Namly
if I wanted to do a `split()` on my input, and parse in one block at a time
or, if I wanted to just use some regexes. In the end I ended setted on regular
expressions. They're slower, for sure, but none of these actions are really
all that speed dependent, and every IRC bot/hipchat bot I've ever interacted
with uses regular expressions, so I figure if it's good enough for them,
it's good enough for me. It's probably fine unless someone decides to troll
everyone and dump in the entire text of 'The Odyessy' or some such. Although
that would be a fun experiment.

Either way, regexes in Python are pretty fast, and now I have three kind of
expensive regexes, as opposed to n pretty fast regexes.

This script looks out for three things:

* @mentions
* (emoticons)
* http://urls.com

and then parses them out to JSON like so:

```
Input:
    "@bob (sadface) did you see this! http://sadnewssite.com

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
```

It does this by taking in the string, and then running the following
regexes on them:

```
mention_re = re.compile(r'(\s@[a-zA-Z]+|^@[a-zA-Z]+)')
emoticon_re = re.compile(r'\([a-zA-Z\d]{1,15}\)')
url_re = re.compile(r'(https?:\/\/\S+)')
```

For mentions and emoticons theres a little post processing for the sake
of formatting, but urls have quite a bit, since URL regexes are actually like
a million lines long. For URLs I parse out what looks like it might be a URL,
then use urlparse as a first pass at validating it, then I attempt to actually
query the URL (to get the title). If it fails because I have a bad connection,
the title gets set to blank and we move on. If it fails because it doesn't
resolve, then I assume its an invalid link and reject it. This is far from
perfect, but its a good start.

It's also worth noting that if a link ends in punctuation, I strip it. I can't
think of a valid URL where that would hose me (in the event of query strings
or hashbangs I would expect either a character to come after them, or for
them to be inconsequential for resolving the page), but it's an edge case to
be aware of.


## Installation

You can either run the setup.py script

```
python ./setup.py install
```

or you can alternatively

```
pip install -r requirements.txt
```


## Usage

You would probably be best served importing it and using it as a function:

```
from hiparser import hiparser

hiparser('some crazy string')
```

Although alternatively you can run it as a script.

```
python ./hiparser/hiparser 'blah blah'
```


## Testing

To run the test suite, simply use setup.py.

```
python ./setup.py test
```


## License

Copyright (c) 2015 Corwin Brown

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
