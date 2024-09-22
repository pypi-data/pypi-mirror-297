# herdmod
A monkeypatcher add-on for pyroherd

## Introduction
herdmod is a compilation of utils i developed for extend my personal use of pyroherd. Then i started to use it and more bots and now i published it to make it easier to be installed in new projects.
It works *together* with pyroherd, this is *not* a fork nor modded version. It does monkey patching to add features to pyroherd classes.

IMPORTANT: you should have installed asyncio pyroherd.

## Usage
Import `herdmod` at least one time in your script, so you'll be able to use modified pyroherd in all files of the same proccess. Example:
```python
# config.py
import herdmod.listen
from pyroherd import Client

app = Client('my_session')
```
```python
# any other .py
from config import app
# no need to import herdmod again, pyroherd is already monkeypatched globally (at the same proccess)
```

I separated the patches between packages to allow you to import only what you want. The `__init__.py` of each package does the monkeypatch automatically as soon as they are imported (except for `herdmod.helpers`, which provides classes and functions that should be explicitely imported).

### `herdmod.listen`
Just import it, it will automatically do the monkeypatch and you'll get these new methods:
- `await pyroherd.Client.listen(chat_id, filters=None, timeout=30)`
Awaits for a new message in the specified chat and returns it
You can pass Update Filters to the filters parameter just like you do for the update handlers. e.g. `filters=filters.photo & filters.bot`

- `await pyroherd.Client.ask(text, chat_id, filters=None, timeout=30)`
Same of `.listen()` above, but sends a message before awaiting
You can pass custom parameters to its send_message() call. Check the example below.

- The bound methods `Chat.listen`, `User.listen`, `Chat.ask` and `User.ask`

Example:
```python
from herdmod import listen # or import herdmod.listen
from pyroherd import Client
client = Client(...)
...
    answer = await message.ask(chat_id, '*Send me your name:*', parse_mode='Markdown')
    await client.send_message(chat_id, f'Your name is: {answer.text}')    
```

### `herdmod.filters`
Import it and the following Update Filters will be monkeypatched to `pyroherd.filters`:

- `filters.dice`
A dice message.

### `herdmod.helpers`
Tools for creating inline keyboards a lot easier.

- `herdmod.helpers.ikb`
Creates a inline keyboard. It's first and only argument must be a list (the keyboard) containing lists (the lines) of buttons.
The buttons can also be lists or tuples. I use tuples to not have to deal with a lot of brackets.
The button syntax must be this: (TEXT, CALLBACK_DATA) or (TEXT, VALUE, TYPE), where TYPE can be 'url' or any other supported button type and VALUE is its value. This syntax will be converted to {"text": TEXT, TYPE: VALUE). If TYPE is CALLBACK_DATA, you can omit it, just like the fist syntax above.
Examples:
```python
from herdmod.helpers import ikb
...
keyboard = ikb([
    [('Button 1', 'call_1'), ('Button 2', 'call_2')],
    [('Another button', 't.me/herdmod', 'url')]
])
await message.reply('Test', reply_markup=keyboard)
```
- `herdmod.helpers.array_chunk`
Chunk the elements of a list into small lists. i.e. [1, 2, 3, 4] can become [[1,2], [3,4]]. This is extremely useful if you want to build a keyboard dinamically with more than 1 column. You just put all buttons together in a list and run:
```python
lines = array_chunk(buttons, 2) # generate a list of lines with 2 buttons on each
keyboard = ikb(lines)
```

### Copyright & License
This project may include snippets of pyroherd code
- pyroherd - Telegram MTProto API Client Library for Python. Copyright (C) 2023-2025 OnTheHerd <<https://github.com/OnTheHerd>>

Licensed under the terms of the [GNU Lesser General Public License v3 or later (LGPLv3+)](COPYING.lesser)
