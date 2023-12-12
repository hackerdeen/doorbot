# Doorbot

How the door gets unlocked.

HW is an ESP32 in nodemcu(ish) form factor running micropython with a relay shield (or hat, or cape, or whatever they're actually called in this form factor).

Code for the ESP32 is in `micropython/` dir.

Needs something to send `ping` messages periodically or it'll reset itself. 

`monitor_doorbot.py` sends `ping` messages and does some reporting to `irccat`. 

There are `example_secrets.py` files for `monitor_doorbot.py` and the micropython that need values filled in and moved to be `secrets.py` for them to work. 
