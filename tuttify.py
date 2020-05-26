import telegram_send, time
import json
import argparse, os
from datetime import date, timedelta

from urllib.request import urlopen
from bs4 import BeautifulSoup

# Parse arguments
parser = argparse.ArgumentParser(
description="This script will watch tutti.ch for new ads and notify you via telegram. Also, it keeps a record of listings with prices in a JSON file."
)
parser.add_argument('query', metavar="Query", type=str, help='tutti.ch search string')
args = parser.parse_args()

# Header for requests
headers = {
    'User-Agent': 'Anon',
    'From': 'youre.mail@here.com'
}

while True:
    # Download page
    try:
        search_url = 'https://www.tutti.ch/de/li/ganze-schweiz?q=' + args.query.lower()
        print(search_url)
        html = urlopen(search_url)
        soup = BeautifulSoup(html, features="lxml")

        list_all = soup.find_all('div', attrs={"class":"_3aiCi"})

        for item in list_all:

            url = item.find_all('a', attrs={"class":"_16dGT"})[0].get("href")
            url = "https://tutti.ch" + url

            title = item.find_all('h4', attrs={"class":"_2SE_L"})[0].get_text()

            price = item.find_all('div', attrs={"class":"_6HJe5"})[0].get_text()

            location = item.find_all('span', attrs={"class":"_3f6Er"})[0].get_text()

            # Create dict for first advertisement
            #new_dict = {"name" : title, "url" : url, "price" : price, "date" : date_pub}
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

            else:
                with open(fname,'r+') as f:
                    dic = json.load(f)

                    if new_dict in dic["inserate"]:
                        print("same..")

                        # If listing is known, skip all afterwards
                        f.close()
                        break
                    else:
                        dic["inserate"].append(new_dict)
                        f.seek(0)
                        json.dump(dic, f)

                        # notify
                        print("New listing...")
                        message = 'Neues Inserat: {} ({}) in {}\n {}'.format(title, price, location, url)
                        telegram_send.send(messages=[message])

            # Close file
            f.close()

        # Wait a minute
        time.sleep(60)

    except:
        # Wait half a minute, in case the server isn't reachable
        print("Server not reachable")
        time.sleep(30)
