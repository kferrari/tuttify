import telegram_send, time
import json
import argparse, os, sys
from datetime import date, timedelta

from urllib.request import urlopen
from bs4 import BeautifulSoup

def ad_known(title):
    for i, d in enumerate(dic["inserate"]):
        if d["name"] == title:
            return 1
    return 0

# Parse arguments
parser = argparse.ArgumentParser(
description="This script will watch tutti.ch for new ads and notify you via telegram. Also, it keeps a record of listings with prices in a JSON file."
)
parser.add_argument('query', metavar="Query", type=str, help='tutti.ch search string')
parser.add_argument('-c', '--canton', metavar="Canton", type=str, default="ganze-schweiz",
    help="In which canton to look for.")
parser.add_argument('-co', '--companyad', metavar="AdType", type=str, default="",
    help="Whether to display company ('true') or private ('false') ads. Leave empty for both.")
parser.add_argument('-f', '--free', action='store_true', default=False,
    help="To only show listings 'for free'.")
parser.add_argument('-l', '--lang', metavar="Language", type=str, default="",
    help="Which language to use. Must be one of 'de', 'fr' or 'it'.")
parser.add_argument('-ma', '--maxprice', metavar="maxPrice", type=int, default=0,
    help="Highest price to still look for.")
parser.add_argument('-mi', '--minprice', metavar="minPrice", type=int, default=0,
    help="Lowest price to still look for.")
parser.add_argument('-n', '--neighbor', action='store_true', default=False,
    help="To include neighboring cantons. Requires -c to be set.")
parser.add_argument('-s', '--silent', action='store_true', default=False,
    help="Don't send notifications.")

args = parser.parse_args()

# Header for requests
headers = {
    'User-Agent': 'Anon',
    'From': 'your.email@here.com'
}

while True:
    try:
        # Build up url with queries
        search_url = 'https://www.tutti.ch/de/li/' + args.canton.lower()

        if args.neighbor:
            search_url += "/nachbarkantone"

        search_url += "/angebote"

        if args.free:
            search_url += "/gratis"

        search_url += "?q=" + args.query.lower().replace(" ", "%20")

        if args.maxprice:
            search_url += "&pe=" + str(args.maxprice)

        if args.minprice:
            search_url += "&ps=" + str(args.minprice)

        if args.lang:
            search_url += "&query_lang=" + args.lang

        if args.companyad:
            search_url += "&company_ad=" + args.companyad

        # Download page
        html = urlopen(search_url)
        soup = BeautifulSoup(html, features="lxml")

        list_all = soup.body.find_all('div', attrs={"class":"p78z0m-0"})

        n_new = 0
        sys.stdout.write("\r {} new listings".format(n_new))

        for item in list_all:

            url = item.find_all('a')[0].get("href")
            url = "https://tutti.ch" + url

            all_text = item.find_all(text=True)
            all_text[:] = (value for value in all_text if value != " ")
            all_text[:] = (value for value in all_text if value != ",")
            all_text[:] = (value for value in all_text if value != ",\xa0")

            location = all_text[1]
            title = all_text[6]
            try:
                price = all_text[8].replace(" ", "")
            except:
                try:
                    price = all_text[7].replace(" ", "")
                except:
                    try:
                        price = all_text[6].replace(" ", "")
                    except:
                        print(all_text)
                        price = "error"

            # Create dict for first advertisement
            new_dict = {"name" : title, "url" : url, "price": price, "location": location}

            # Check if file exists already and create if not
            fname = args.query.lower() + "_dictionary.json"
            if not os.path.isfile(fname):
                mydict = {}
                mydict["inserate"] = []
                listings = mydict["inserate"]
                listings.append(new_dict)

                with open(fname, 'w') as f:
                    json.dump(mydict, f)

                # notify
                n_new += 1
                sys.stdout.write("\r {} new listings".format(n_new))

                if not args.silent:
                    message = 'Neues Inserat: {} ({}) in {}\n {}'.format(title, price, location, url)
                    telegram_send.send(messages=[message])

            else:
                with open(fname,'r+') as f:
                    dic = json.load(f)

                    if ad_known(title):
                        # do nothing
                        pass

                    else:
                        dic["inserate"].append(new_dict)
                        f.seek(0)
                        json.dump(dic, f)

                        # notify
                        n_new += 1
                        sys.stdout.write("\r {} new listings".format(n_new))

                        if not args.silent:
                            message = 'Neues Inserat: {} ({}) in {}\n {}'.format(title, price, location, url)
                            telegram_send.send(messages=[message])

            # Close file
            f.close()

        # Wait a minute
        time.sleep(60)

    except:
        # Wait half a minute, in case the server isn't reachable
        sys.stdout.write("\rServer not reachable or other error")
        time.sleep(30)
