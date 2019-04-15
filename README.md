## greeting.py ##
This module greets users with a preset message when they speak within X seconds of joining a channel Sopel is in, or when someone uses the !greet command

TODO
* Fix nick tracking (joining, changing nick, then speaking within timeout does not trigger greeting)


## steamstatus.py ##
This module retrieves steamstat.us info and [presents it nicely](https://imgur.com/a/TKnsRLM)


## faq.py ##
A *very* simple FAQ module 


## admin_mod.py ##
So far, this module simply serves to add a `say` alias to the `msg` command from the `admin` module. All commands from `admin` are loaded through here, so do not load the `admin` module as well.
