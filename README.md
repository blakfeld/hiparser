# Hiparser (HipChat Parser)

A fun script to emulate parsing out commands from a chat client.

I went through a few variations on how I wanted to handle the parsing. Namly
if I wanted to do a `split()` on my input, and parse in one block at a time,
but I ended up settling on regular expressions. They're slower, for sure, but
none of these actions are really all that speed dependent, and every
IRC bot/hipchat bot I've ever interacted with uses regular expressions,
so I figure if it's good enough for them, it's good enough for me. It's
probably fine unless someone decides to troll everyone and dump in the entire
text of 'The Odyessy' or some such. Although that would be a fun experiment.


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
