# tuttify

Tired of being notified too late about new listings of your favourite things?

Use tuttify.py to scrape tutti.ch for new listings and alert you via Telegram.

### Install

* Clone this repo or download tuttify.py.
* Edit lines 18 and 19 in tuttify.py to include your name and email address, if you want. This is good practice in case someone over at tutti.ch wants to contact you.
* Install [telegram-send](https://pypi.org/project/telegram-send/) and run `telegram-send --configure` to set up your personal Bot.
* Install [beautifulsoup](https://pypi.org/project/beautifulsoup4/).

### Usage

Simple run:

```bash
python3 tuttify.py -q sofa

python3 tuttify.py -q "raspberry pi 4"
```

To run in background:

```bash
nohup python3 -u tuttify.py -q sofa &
```

The first run will build the dictionary of existing listings and save it to a JSON file. It also sends a message for each listing. To only build the dictionaryof existing listing, use the `--silent` flag.

```bash
python3 tuttify.py -q sofa --silent
```

To only search a specific canton, use the `--canton` parameter

```bash
python3 tuttify.py -q sofa --canton graubuenden
```

To define a maximum price, use `--maxprice`

```bash
python3 tuttify.py -q sofa --canton graubuenden --maxprice 50
```
