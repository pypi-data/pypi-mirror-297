## Features

- 🎈 Lightweight: No heavy dependencies, plug and play!
- 🎯 Zero-overhead: No overhead if you turn it off!
- 👨‍🎓 Structured: Use output format **defined by you**. You master every detail!
- 🔧 Flexible and easy for use. Just `logger.log("witness", variables)`! Witlog will automatically organize them.

## Installation

Simply `pip install witlog`

## Usage

### Quick Start

```py
import witlog as wl
from witlog import StaticLogger

logger = StaticLogger([
            "layer_idx",
            ["x","y"] * 5,
            "post_scores",
            ...
        ], print)#print for example
wl.register_logger('CHECK_SCORES', logger)

... ##your code

with wl.monitor('CHECK_SCORES') as logger:
    logger.log('layer_idx', layer)

for i in range(5):
    ##do sth
    with wl.monitor('CHECK_SCORES') as logger:
        logger.log('x', x)
        logger.log('y', y)
with wl.monitor('CHECK_SCORES') as logger:
    logger.log('post_scores', post_scores)
```

This example code would print all variables, because `print` is passed as `output_func`.

Let's have a quick view of the signature of `StaticLogger`:

```py
class StaticLogger:
    def __init__(self, template, output_func):
        ...
```

`template` is a list, the format will be elaborated later. `output_func` is a callable which will receive a `LogBlock`(your logging result) object. We also offer a `PickleTo` helper class for better saving. You can access it by `wl.PickleTo`.

The overall workflow is:

1. define your logging format.
2. define your output_func.
3. register logger.
4. use `monitor` when programming and simply `logger.log(key, value)`.

Monitor will return a default logger if no logger is registered. And this logger will do nothing.

If you want to disable a logger, it's quite easy: `tl.remove_register(name)`.

### Main Concepts

Witlog considers code as many loops(including nested loop), and hence logs can be structured as *blocks*. Each block corresponds to a loop in code.

So, the code below

```py
print(x)
for i in range(K):
    print(y)

print(z)
```

can be seen as :

```py
[
    item,
    block,
    item
]
```

Naturally, we can come up with such a definition:

1. The log message unit is *Message*. A message is indivisible.
2. Each *Block* consists of **ordered** Message and Block.
3. A Message is a Block.

Hence, we can define log format as a list:

```py
[
    "name1",
    ["a", "b"] * m,
    "samples"...
]
```

Since python code is executed orderedly, logging when running has same order as traversing this list. Thus, we can get a well-structured log. 

This has an advantage when use: you ONLY need to specify the `name` when logging, ignoring the actual tree-like structure. It's very convenient like:

```py
with wl.monitor("SCORES") as logger:
    logger.log('a', a)
```

This means you don't need to care about other code affection when developing.

In implementation, *Block* is corresponding to `LogBlock`, *Message* is corresponding to `LogMsg`. Both have a property `content`, including the actual object(s) they store. `LogMsg` has a `name` but `LogBlock` is anonymous.

### Post-processing

Witlog's biggest advantage lies in its simple post-processing. You can easily extract the data you need from the structured `LogBlock`, rather than manually writing cumbersome analysis scripts.

Say you've got a `LogBlock` defined by:

```py
[
    'outer_loop_idx',
    ['inner_x'] * 10,
    'final_flag'
]
```

and you want extract 5th `inner_x`:

```py
print(block[1][5].content)
```

If you want to get the content associating to a *unique* name, such as `final_flag`, it's easier and more readable:

```py
print(block['final_flag'].content)
```

But if you want to extract content associating to duplicate names, the default indexing would only return the first match. This is not recommended.

### Convention

1. No expression in `log(key, value)`. Expressions would be always executed(even if you remove the register), and that might cause unexpected overhead. The best practice is simple string for key and only object for value. A common mistake is f-string. If you really want to combine something, we recommend you to implement a custom logger.
2. Use `with wl.monitor(name)` instead of `get_logger`. The latter one would work and reduce some coding effort indeed, but `with` create a block of code. It's more readable, and allowing "truly zero-overhead". Though skipping `with` is rejected in [PEP-343](https://peps.python.org/pep-0343/), there is will some space for hacking code stack. It's dangerous so will not be integrated into witlog, but maybe we can achieve this safely some day 😉

Hope witlog simplify your code and project 🌹