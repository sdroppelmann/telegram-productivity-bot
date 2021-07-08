# Telegram Productivity Bot
A bot that reminds you to take breaks. Yeah, that pretty much it.

## Dependencies
[Telepot](https://telepot.readthedocs.io/en/latest/)

## Usage
```shell
python3 bot.py token=<YOUR_BOT_TOKEN> userid=<YOUR_USER_ID>
```

## Commands
Note that all commands are case-insensitive, so /setBreakInterval works the same as /setbreakinterval
```shell
/workmode                     // toggle workmode on and off
/workmode on                  // start workmode
/workmode off                 // stop workmode

/setbreakinterval <MINUTES>   // set time in minutes for break reminder, default is 60, so 1h

/shutdown                     // terminates the bot

/status                       // show current break interval as well as some additional information

/continue                     // equal to '/workmode on', but shorter
```
