# tuttify

Tired of being notified too late about new listings of your favourite things?

Use tuttify.py to scrape tutti.ch for new listings and alert you via Telegram.

### Install

* Clone this repo or download tuttify.py.
* Edit lines 18 and 19 in tuttify.py to include your name and email address, if you want. This is good practice in case someone over at tutti.ch wants to contact you.
* Install [telegram-send](https://pypi.org/project/telegram-send/) and run `telegram-send --configure` to set up your personal Bot.
* Install [beautifulsoup](https://pypi.org/project/beautifulsoup4/).

### Usage

Simple run

```bash
python3 tuttify.py sofa

python3 tuttify.py "raspberry pi 4"
```

To run in background

```bash
nohup python3 -u tuttify.py sofa &
```

The first run for each unique query will build a dictionary of existing listings and save it to a JSON file. It also sends a message for each listing. To avoid cluttering of your Telegram conversation, use the `--silent` flag first. Later, re-run without the flag to only be notified about new listings.

```bash
python3 tuttify.py sofa --silent
```

To only show listings for free

```bash
python3 tuttify.py sofa -f
```

To only search a specific canton, use `--canton`. Use `-n` to also include neighboring cantons.

```bash
python3 tuttify.py sofa --canton graubuenden -n
```

To define a price range, use `--maxprice` and/or `--minprice`

```bash
python3 tuttify.py sofa --minprice 10 --maxprice 150
```

To only show ads from private sellers, use `--companyad false`

```bash
python3 tuttify.py sofa --companyad false
```
