import urllib.request
import json
import csv
import time
from urllib.error import URLError
# structure id: 60003760 	Jita IV - Moon 4 - Caldari Navy Assembly Plant
# region_id for the Forge: 10000002


class Order:
    def __init__ (self,json_data):
        self.type_id = json_data["type_id"]
        self.location_id = json_data["location_id"]
        self.price = json_data["price"]
        self.is_buy_order = json_data["is_buy_order"]

#-------------------------------------------------------------------------------

filename = "test_input.txt"
type_id_dict = {}
with open(filename, "r") as tsv:
    data = csv.reader(tsv, delimiter="\t")
    for line in data:
        type_id_dict[line[0]] = line[1]

base_url = "https://esi.tech.ccp.is/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&page=1&type_id="

#f = open("arbitrage.txt", "a+")
#f.write("type_id,   type_id_dict[type_id],  profit,     margin")

for type_id in type_id_dict:
    site = base_url + type_id
    print(site)
    try:
        r = urllib.request.urlopen(site)
    except URLError as error:
        print(error)
    else:    
        raw_json = json.load(r)
        
    obj_list = []
    for entry in raw_json:
        obj_list.append(Order(entry))
    

#    for obj in obj_list:
#        print(obj.type_id, obj.price, obj.is_buy_order)

##########################################################
    speculative_list = []
    sell_min = -1
    buy_max = -1
    for obj in obj_list:

        if obj.is_buy_order == True:
            if obj.price == -1:
                buy_max == obj.price
            elif obj.price > buy_max:
                buy_max = obj.price
        elif obj.is_buy_order == False:
            if obj.price == -1:
                sell_min = obj.price
            elif obj.price < sell_min:
               sell_min = obj.price
    print(buy_max, sell_min)
#    profit = sell_min - buy_max
#    margin = profit/sell_min
#    if (margin > .50 and sell_min != 99999999999999999999 and buy_max != 0.001):
#        print(type_id_dict[type_id], profit, margin)
#        print('{0:5} {1:32} \t {2:16.2f} \t {3:.2f}'.format(type_id,
#                                                type_id_dict[type_id],
#                                                profit,
#                                                margin))
#        speculative_list.append([type_id, type_id_dict[type_id], profit, margin])
        #f.write(str([type_id, type_id_dict[type_id], sell_min - buy_max, margin] ))
    r.close()


