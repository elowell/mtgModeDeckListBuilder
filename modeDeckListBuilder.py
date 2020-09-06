
import requests
import argparse
import re
import csv
import urllib.parse
from urllib.parse import urlparse
from bs4 import BeautifulSoup as BS

def get_deck_links(site, commander_url, decks, titles, url_theme):
    if site.lower() == 'archidekt':
        pass
    elif site.lower() == 'tappedout':
        url_tappedout = 'https://tappedout.net'
        url_prefix = 'https://tappedout.net/mtg-decks/search/?q=&format=edh&general='
        url_suffix = '&price_min=&price_max=&o=-Views&submit=Filter+results'
        if url_theme == '&hubs=':
            url_theme = ""
        # url_example = 'https://tappedout.net/mtg-decks/search/?q=&format=edh&general=trostani-selesnyas-voice&price_min=&price_max=&o=-Views&submit=Filter+results'
        url = url_prefix + commander_url + url_suffix
        url_deck_suffix = '?cat=type'
        try:
            r = requests.get(url, verify=True)
            if r.status_code == 200:
                soup = BS(r.text, features="lxml")
                a = soup.find_all("a", href=re.compile("/mtg-decks/"))
                for link in a:
                    link_title = str(link.get("title"))
                    if link_title.startswith("mtg decks - "):
                        titles.append(link_title.strip('mtg decks - '))
                        decks.append(url_tappedout + link.get('href')+url_deck_suffix)
        except Exception as ex:
            print(str(ex))

def get_deck_list_tappedout(url, decks):
    try:
        r = requests.get(url, verify=True)
        if r.status_code == 200:
            soup = BS(r.text, features="lxml")
            creatures = soup.find_all("ul",{"class": "boardlist"}) # values we want are within contents, but tedious to pull out info
            print("stop")
    except Exception as ex:
        print(str(ex))

def decklist_import(url, decks, site = "tappedout"):
    if site == "tappedout":
        card_flag = False
        cards = []
        try:
            copy_url= url+"#embed-modal"
            r = requests.get(copy_url, verify=True)
            if r.status_code == 200:
                soup = BS(r.text, features="lxml")
                deck_text = soup.find(id = 'mtga-textarea')
                cards = deck_text.text.split('\n')
                cards = [card[0:card.rfind('(')] for card in cards]
                if not cards:
                    print("no cards found at url %s" % url)
                else:
                    cards_total = len(cards)
                    for card_str in cards:
                        if card_str is not "":
                            card_count, card = card_str.split(' ', 1)
                            card = card.rstrip()
                            if (card).startswith('Snow-Covered '):
                                card = card.strip('Snow-Covered ')
                            decks[card] = decks.get(card, 0) + int(card_count)
        except Exception as ex:
            print(str(ex))
    else:
        pass

if __name__ == '__main__':
    # Create Arg Parser and add arguments
    parser = argparse.ArgumentParser(description="Magic the Gathering Commander Mode Decklist Generator\n Commander input (-c) is always required")
    parser.add_argument('-c','--commander', help='Input commander name here with quotes around it. Needs to be accurate', required=True)
    parser.add_argument('-s','--sites', nargs='*', default=['tappedout', 'archidekt'], help='Specific sites to use. Options currently include tappedout. Defaults to all sites', required=False)
    parser.add_argument('-t', '--themes', nargs='*', default=[], help='Specify which themes to use. They should be spaced out. Defaults to all', required=False)
    parser.add_argument('-o','--overwrite', default=True, help = 'Overwrite existing file? True/False. Defaults to True')
    args = vars(parser.parse_args())
    # Create Commander url insert
    commander = args['commander'].replace(',',"")
    commander_url = re.sub(r"[^\w\s]", '', commander)
    commander_url = (re.sub(r"\s+", '-', commander_url)).lower()
    #handle any provided themes
    themes = args['themes']
    theme_str = ""
    theme_url = ""
    for theme in themes:
        theme_url += "&hubs="+theme
        theme_str += theme + ","
    theme_str = " " + theme_str.rstrip(",")
    # Overwrite/truncate file at end?
    overwrite = 'w+'
    if not args['overwrite']:
        overwrite = 'w'
    #initialize variables
    deck_links = []
    titles = []
    mode_deck = {}
    decks_imported = 0
    basic_lands = ['Swamp','Forest','Island', 'Mountain', 'Plains']
    # decks = {'creature':[], 'sorcery':[], 'instant':[], 'enchantment':[], 'planeswalker':[],'artifact':[],'land':[]}
    for site in args['sites']:
        get_deck_links(site, commander_url, deck_links, titles, theme_url)
    for i in range(len(deck_links)):
        link = deck_links[i]
        decklist_import(link, mode_deck)
        decks_imported += 1
        print("finished importing deck: %s " % titles[i])
    mode_deck_list = sorted(mode_deck.items(), key=lambda x:x[1], reverse=True)
    [print(key, value) for (key, value) in mode_deck_list]
    with open(commander+theme_str+".csv", 'w+', newline='') as myfile:
        csv_out = csv.writer(myfile)
        csv_out.writerow(["Decks imported:", decks_imported])
        csv_out.writerow(["Themes Used: ", theme_str.lstrip(" ")])
        csv_out.writerow(["Basic Land", "Avg Count"])
        for land in basic_lands:
            if land in mode_deck:
                land_avg = mode_deck[land]/decks_imported
                csv_out.writerow([land, land_avg])
        csv_out.writerow(['Card','Count'])
        csv_out.writerows(mode_deck_list)
    print("Finished!")


            # for i in a:
            #     k = i.get('href')
            #     try:
            #         m = re.search("(?P<url>https?://[^\s]+)", k)
            #         n = m.group(0)
            #         rul = n.split('&')[0]
            #         domain = urlparse(rul)
            #         if(re.search('tappedout.net', domain.netloc)):
            #             continue
            #         else:
            #             deck_links.append(rul)
            #     except:
            #         continue

