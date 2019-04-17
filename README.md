## Modules
* [greeting.py](#greeting)
* [steamstatus.py](#steamstatus)
* [faq.py](#faq)
* [admin_mod.py](#admin_mod)
## Other 
* [Ideas for stuff to write](#ideas)

### greeting
This module greets users with a preset message when they speak within X seconds of joining a channel in the whitelist, or when someone uses the `greet` command

TODO
* Fix nick tracking (joining, changing nick, then speaking within timeout does not trigger greeting)


### steamstatus
This module retrieves steamstat.us info and [presents it nicely](https://imgur.com/a/TKnsRLM)

TODO
* Add cache, with configurable TTL

### faq
A *very* simple FAQ module 

TODO
* Per [708b4c5](https://github.com/squigglezworth/sopel-modules/commit/708b4c5cbc15fb2f9caec23e99ccc12b976d5c6e), determine another way of loading the questions/answers while still allowing the admin to update the data

### admin_mod
So far, this module simply serves to add a `say` alias to the `msg` command from the `admin` module. All commands from `admin` are loaded through here, so do not load it as well. 

(*If we don't `import *` from the `admin` module, commands that are modified in this module will be executed twice.*)

TODO 

* Find cleaner way of importing from `admin`
* Allow calling commands without PRIVMSG


## Ideas
