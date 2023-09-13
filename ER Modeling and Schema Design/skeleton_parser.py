
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

item_dict = {}
seller_dict = {}
bidder_dict = {}
bids_dict = {}
category_dict = {}
item_string = ""
bidder_string = ""
seller_string = ""
category_string = ""
bids_string = ""

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def stringFix(string):
    if string is None or len(string) == 0:
        return "NULL"
    else:
        return '"' + string.replace('"', '""') + '"'

def seller_table(item):
    seller_values = [] #Country, Rating, Location
    if "Seller" in item and item['Seller'] != None: #check if there is a valid seller
        seller_keys = list(seller_dict.keys())
        userID = stringFix(item['Seller']['UserID'])
        if userID not in seller_keys: #create a new dict key,val pair
            seller_dict[item['Seller']['UserID']] = []
            
        if "Country" in item and item['Country'] != None:
            seller_values.append(stringFix(item['Country']))
        else:
            seller_values.append('null')
            
        if "Rating" in item['Seller'] and item['Seller']['Rating'] != None:
            seller_values.append(str(item['Seller']['Rating']))
        else:
            seller_values.append('null')
            
        if "Location" in item and item['Location'] != None:
            seller_values.append(stringFix(item['Location']))
        else:
            seller_values.append('null')
            
        seller_dict[userID] = seller_values # userID: [Name,Rating,Location]
        string = str(userID) + "|" + str(seller_values[0]) + "|" + str(seller_values[1]) + "|" + str(seller_values[2]) + "\n"
        #print(string)
        global seller_string
        seller_string += string
    return
    
def bidder_table(item):
    if 'Bids' in item and item['Bids'] != None:
        for bidder in item['Bids']:
            bidder_values = [] #Country, Rating, Location
            if "Bidder" in bidder['Bid'] and bidder['Bid']['Bidder'] != None: #check if there is a valid bidder
                bidder_keys = list(bidder_dict.keys())
                userID = stringFix(bidder['Bid']['Bidder']['UserID'])
                if userID not in bidder_keys: #create a new dict key,val pair
                    bidder_dict[bidder['Bid']['Bidder']['UserID']] = []
            
                if "Country" in bidder['Bid']['Bidder'] and bidder['Bid']['Bidder']['Country'] != None:
                    bidder_values.append(stringFix(bidder['Bid']['Bidder']['Country']))
                else:
                    bidder_values.append('null')
            
                if "Rating" in bidder['Bid']['Bidder'] and bidder['Bid']['Bidder']['Rating'] != None:
                    bidder_values.append(str(bidder['Bid']['Bidder']['Rating']))
                else:
                    bidder_values.append('null')
            
                if "Location" in bidder['Bid']['Bidder'] and bidder['Bid']['Bidder']['Location'] != None:
                    bidder_values.append(stringFix(bidder['Bid']['Bidder']['Location']))
                else:
                    bidder_values.append('null')
            
                bidder_dict[userID] = bidder_values # userID: [Name,Rating,Location]
                string = str(userID) + "|" + str(bidder_values[0]) + "|" + str(bidder_values[1]) + "|" +  str(bidder_values[2]) + "\n"
                global bidder_string
                bidder_string += string
    return

def items_table(item):
    item_values = [] #Name, Started, Ends, Description, Currently, First_Bid, Number_of_Bids, Buy_Price, Seller, Location
    if "ItemID" in item and item['ItemID'] != None: #check if there is a valid bidder
        item_keys = list(item_dict.keys())
        if item['ItemID'] not in item_keys: #create a new dict key,val pair
            item_dict[item['ItemID']] = []
            
        if "Name" in item and item['Name'] != None:
            item_values.append(stringFix(item['Name']))
        else:
            item_values.append('null')
            
        if "Started" in item and item['Started'] != None:
            start = transformDttm(item['Started'])
            item_values.append(start)
        else:
            item_values.append('null')
            
        if "Ends" in item and item['Ends'] != None:
            end = transformDttm(item['Ends'])
            item_values.append(end)
        else:
            item_values.append('null')
            
        if "Description" in item and item['Description'] != None:
            item_values.append(stringFix(item['Description']))
        else:
            item_values.append('null')
            
        if "Currently" in item and item['Currently'] != None:
            currently = transformDollar(item['Currently'])
            item_values.append(currently)
        else:
            item_values.append('null')
            
        if "First_Bid" in item and item['First_Bid'] != None:
            fb = transformDollar(item['First_Bid'])
            item_values.append(fb)
        else:
            item_values.append('null')
            
        if "Number_of_Bids" in item and item['Number_of_Bids'] != None:
            item_values.append(str(item['Number_of_Bids']))
        else:
            item_values.append('null')
            
        if "Buy_Price" in item and item['Buy_Price'] != None:
            bp = transformDollar(item['Buy_Price'])
            item_values.append(bp)
        else:
            item_values.append('null')
            
        if "Seller" in item and item['Seller'] != None: #check if there is a valid seller
            item_values.append(stringFix(item['Seller']['UserID']))
        else:
            item_values.append('null')    
        
        if "Location" in item and item['Location'] != None:
            item_values.append(stringFix(item['Location']))
        else:
            item_values.append('null')

        if "Country" in item and item['Country'] != None:
            item_values.append(stringFix(item['Country']))
    
    item_dict[item['ItemID']] = item_values # itemID: [Name, Started, Ends, Description, Currently, First_Bid, Number_of_Bids, Buy_Price, Seller, Location]
    string = str(item['ItemID']) + "|" +  str(item_values[0]) + "|" + str(item_values[1]) + "|" +  str(item_values[2]) + "|" + str(item_values[3]) + "|" + str(item_values[4]) + "|" + str(item_values[5]) + "|" + str(item_values[6]) + "|" + str(item_values[7]) + "|"  + str(item_values[8]) + "|" + str(item_values[9]) + "|" + str(item_values[10]) + "\n"
    global item_string
    item_string += string
    return

def category_table(item):
    #key (ItemID, Category)
    if 'ItemID' in item and item['ItemID'] != None:
        for cat in item['Category']:
            ci_tup = (item['ItemID'], cat)
            category_dict[ci_tup] = []
            string = str(ci_tup[0]) + "|" + stringFix(str(ci_tup[1])) + "\n"
            global category_string
            category_string += string

    #categories_dict[item['ItemID']] = cat_val
    return


def bids_table(item):
    #key (ItemID, UserID, Time)
    bid_values = [] #Amount
    if 'Bids' in item and item['Bids'] != None:
        for bid in item['Bids']:
            itemID = item['ItemID']
            biduserID = bid['Bid']['Bidder']['UserID']
            time = 'null'
            if bid['Bid']['Time'] != None:
                time = transformDttm(bid['Bid']['Time'])
                
            amount = 'null'
            if bid['Bid']['Amount'] != None:
                amount = transformDollar(bid['Bid']['Amount'])
            bid_values.append(amount)
            
            b_tup = (itemID, biduserID, time)
            bids_dict[b_tup] = bid_values
            string = stringFix(str(b_tup[0])) + "|" + stringFix(str(b_tup[1])) + "|" + str(b_tup[2]) + "|" +  str(bid_values[0]) + "\n"
            global bids_string
            bids_string += string
    return
    
    
"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    global item_dict, seller_dict, bidder_dict, bids_dict, category_dict
    global item_string
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            #5 Tables = 5 .dat files
            #bidder
            #seller
            #category
            #items
            #bids
            items_table(item)
            bidder_table(item)
            seller_table(item)
            category_table(item)
            bids_table(item)

            
# def sellers_to_text(d):
#     string = ""
#     for seller_key in d:
#         values = d[seller_key]
#         string = string + '"' + str(seller_key) + '"' + "|" + '"' + str(values[0]) + '"' + "|" + str(values[1]) + "|" + '"' +  str(values[2]) + '"' + "\n"
#     return string
    
# def items_to_text(d):
#     string = ""
#     for item_key in d:
#         values = d[item_key]
#         string = string + str(item_key) + "|" + '"' + str(values[0]) + '"' + "|" + str(values[1]) + "|" + '"' +  str(values[2]) + '"' + "|" + '"' + str(values[3]) + '"' + "|" + str(values[4]) + "|" + str(values[5]) + "|" + str(values[6]) + "|" + str(values[7]) + "|" + '"' + str(values[8]) + '"' + "|" + '"' + str(values[9]) + '"' + "\n"
#     return string
    

# def bids_to_text(d):
#     string = ""
#     for bid_key in d:
#         values = d[bid_key]
#         string = string + str(bid_key[0]) + "|" + '"' + str(bid_key[1]) + '"' + "|" + '"' + str(bid_key[2]) + '"' + "|" +  str(values[0]) + "\n"
#     return string
        
            
# def c_to_text(d):
#     string = ""
#     for c_key in d:
#         values = d[c_key]
#         string = string + str(c_key[0]) + "|" + '"' + str(c_key[1]) + '"' + "\n"
#     return string
            



"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)
    
#     stext = sellers_to_text(seller_dict)
# #     print(stext)
    sellers = open("sellers.dat", "w")
    sellers.write(seller_string)
    sellers.close()

    #print(seller_string)
    
#     btext = sellers_to_text(bidder_dict)
# #     print(btext)
    bidders = open("bidders.dat", "w")
    bidders.write(bidder_string)
    bidders.close()
    
    #print(bidder_string)
    
    #itext = items_to_text(item_dict)
#     print(item_string)
    items = open("items.dat", "w")
    items.write(item_string)
    items.close()

    #print(item_string)
    
#     bidstext = bids_to_text(bids_dict)
# #     print(bidstext)
    bids = open("bids.dat", "w")
    bids.write(bids_string)
    bids.close()

    #print(bids_string)


#     #print(category_dict)
#     ctext = c_to_text(category_dict)
#     #print(ctext)
    cat = open("category.dat", "w")
    cat.write(category_string)
    cat.close()

    #print(category_string)
    
    #fix_quotes("sellers.dat")
    #fix_quotes("bidders.dat")
    # fix_quotes("items.dat")
    # fix_quotes("bids.dat")
    # fix_quotes("category.dat")
    
    
    
if __name__ == '__main__':
    main(sys.argv)
