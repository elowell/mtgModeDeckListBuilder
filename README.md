# mtgModeDeckListBuilder
Command line tool for creating "mode" EDH decklist based on top decks for a specific commander. This grabs top decklists for specified commander and returns a csv with sorted list of cards that are used. It also provides information on average number of basic lands run across the decks. Currently only works for tappedout.net, but functionality for archidekt coming soon.

Runs on Python 3.6 and requires the following libraries: requests, argparse, re, csv, urlib, and bs4 (Beautiful Soup)

Required arguments:
  - Commander argument: ```-c <commander name in quotes>``` -- the commander you want a mode dekclist for.

Optional arguments:
  - Theme argument: ```-t <themes in quotes separated by spaces>``` -- Use this if you want to specify specific themes/hubs. Themed searches create a unique csv file name.
  - Sites argument: ```-s <sites in quotes separated by spaces>``` -- Use this if you want to specify specific sites. Defaults to all sites available
  - Overwrite argument: ```-o <True/False>``` -- Use if you don't want to overwrite/truncate existing csv file. Defaults to true. 

Example commands:
  -```python mtgModeDeckListBuilder.py -c "Trostani, Selesnya's Voice" -t "tokens" "Lifegain"```
  -```python mtgModeDeckListBuilder.py -c "Muldrotha, the Gravetide" -s "tappedout" -o False```
