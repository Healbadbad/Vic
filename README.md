# VIC
## Visual Interaction with Code
A simple tool for debugging and interacting with running python code.

This tool is designed to make it easy to inspect the state of a running python program at any point.
It is not inteded to allow stepping through the execution of code, but to make it easier to find the 
cause of errors, and make them easier to fix.

You can 
  - inspect the currently loaded modules, local variables, and functions/callables
  - inspect individual objects and their attributes
  - show callable properties, and access their signatures and docstrings 

Screenshot:
<Screenshot goes here>


## Usage:
```
from vic import vic
vic.interact(locals())
```


Install from URL:

`pip install git+https://github.com/Healbadbad/Vic`