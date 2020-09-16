import json
import os

# initial setup
personal_file = "countries.json"
vnos = input("Enter a filename of your personal collection in JSON. Leave blank if it is countries.json: ")
if vnos != "":
    if os.access(vnos, os.R_OK):
        personal_file = vnos
    else:
        print("File can not be opened")
        exit(1)

# initializing all lists, sets and dictionaries
all_coin_ids = set()
owned_coin_ids = set()

all_countries_ids = dict()
owned_countries_ids = dict()

coins = dict()

# opening and storing the full list
with open(".countries_full.json") as json_file:
    data = json.load(json_file)
    for country in data:
        collection = data[country]['coins']
        for coin_temp in collection:
            coin = coin_temp["coin"]
            coin_id = coin["id"]
            country = coin_temp["country"]
            value = coin_temp["value"]
            commemorative = coin_temp["commemorative"]
            special_marking = coin["special_marking"]
            year = coin["issued_from"]
            order_no = coin["order_no"]

            all_coin_ids.add(coin_id)
            if country not in all_countries_ids.keys():
                all_countries_ids[country] = set()
            all_countries_ids[country].add(coin_id)

            if commemorative == 1 or commemorative != 0:
                coins[coin_id] = coin_id, year, "commemorative", country
            elif special_marking is not None:
                coins[coin_id] = coin_id, year, country, value, special_marking
            else:
                coins[coin_id] = coin_id, year, country, value

# opening and storing the personal list
with open(personal_file) as json_file:
    data = json.load(json_file)
    for country in data:
        collection = data[country]['coins']
        for coin_temp in collection:
            coin = coin_temp["coin"]
            coin_id = coin["id"]
            country = coin_temp["country"]
            value = coin_temp["value"]
            commemorative = coin_temp["commemorative"]
            year = coin["issued_from"]
            order_no = coin["order_no"]

            owned_coin_ids.add(coin_id)
            if country not in owned_countries_ids.keys():
                owned_countries_ids[country] = set()
            owned_countries_ids[country].add(coin_id)

collected_coins = len(all_coin_ids.intersection(owned_coin_ids))
print("\nYou currently have", collected_coins, "of", len(all_coin_ids), "coins (%1.2f%%)." % (collected_coins/len(all_coin_ids)*100))
if input("Do you want statistics per country? (Y/N, 1/0): ") in ("Y", "y", "1"):
    for country in sorted(all_countries_ids.keys()):
        if country in owned_countries_ids.keys():
            collected_temp = len(all_countries_ids[country].intersection(owned_countries_ids[country]))
            print("%s: %d/%d (%1.2f%%)" % (country, collected_temp, len(all_countries_ids[country]), (collected_temp/len(all_countries_ids[country]))*100))

if input("Do you want a list of missing coins? (Y/N, 1/0): ") in("Y", "y", "1"):
    for id in sorted(all_coin_ids.difference(owned_coin_ids)):
        print(coins[id])

if input("Would you like to see missing coins by value? (Y/N, 1/0): ") in ("Y", "y", "1"):
    value_temp = input("Which value are you interested in? (In cents or 'commemorative'/'cc'): ")
    if value_temp in ("commemorative", "cc", "CC"):
        for id in sorted(all_coin_ids.difference(owned_coin_ids)):
            if coins[id][2] == "commemorative":
                print(coins[id][1], coins[id][3])
    else:
        value_temp = int(value_temp)
        for id in sorted(all_coin_ids.difference(owned_coin_ids)):
            if coins[id][3] == value_temp:
                if len(coins[id]) == 5:
                    print(coins[id][2], coins[id][4])
                else:
                    print(coins[id][2])