"""
"""
import urllib.request
import json
import csv
import time
from urllib.error import URLError
# structure id: 60003760 	Jita IV - Moon 4 - Caldari Navy Assembly Plant
# region_id for the Forge: 10000002


type_id_dict = {}
with open("type_id.txt", "r") as tsv:
    data = csv.reader(tsv, delimiter="\t")
    for line in data:
        type_id_dict[line[0]] = line[1]

base_url = "https://esi.tech.ccp.is/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&page=1&type_id="

f = open("arbitrage.txt", "a+")
f.write("type_id,   type_id_dict[type_id],  profit,     margin")

for type_id in type_id_dict:
    site = base_url + type_id
    try:
        r = urllib.request.urlopen(site)
    except URLError as error:
        print(error)
    else:    
        raw_json = json.load(r)

# I need to error check for the following:
#   --items with no buy and/or sell orders
#   --items with
# Check if location_id == 60003760 (JITA IV Caldari Navy Assembly Plant)


    speculative_list = []
    sell_min = 99999999999999999999
    buy_max = 0.001
    for entry in raw_json:   
        if entry["is_buy_order"] == True:
            if entry["price"] > buy_max:
                buy_max = entry["price"]
        else:
            if entry["price"] < sell_min:
               sell_min = entry["price"]

    profit = sell_min - buy_max
    margin = profit/sell_min
    if (margin > .50 and sell_min != 99999999999999999999 and buy_max != 0.001):
        #print(type_id_dict[type_id], profit, margin)
        print('{0:5} {1:32} \t {2:16.2f} \t {3:.2f}'.format(type_id, 
                                                type_id_dict[type_id], 
                                                profit, 
                                                margin)) 
        speculative_list.append([type_id, type_id_dict[type_id], profit, margin])
        #f.write(str([type_id, type_id_dict[type_id], sell_min - buy_max, margin] ))
    r.close()

for item in speculative_list:
    f.write(item)
f.close()

print("DONE!")
