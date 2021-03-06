import urllib
import pycurl
import json
from pprint import pprint
from pymongo import MongoClient
import crawler3
from crawler3 import *

#url = "https://api.zomato.com/v1/search.json?city_id=1"#&cuisine_id=55&category=2&start=1&count=10"

def getHotels(url):
    client = MongoClient()
    db = client.zomato
    collection = db.hotels
    pycurl_connect = pycurl.Curl()
    pycurl_connect.setopt(pycurl.URL, url)
    pycurl_connect.setopt(pycurl.HTTPHEADER, ['X-Zomato-API-Key: 7749b19667964b87a3efc739e254ada2'])


    with open('/Users/prady/Desktop/output.txt', 'w') as f:
        pycurl_connect.setopt(pycurl_connect.WRITEFUNCTION, f.write)
        pycurl_connect.perform()


    with open('/Users/prady/Desktop/output.txt') as data_file:    
        data = json.load(data_file)

    null=0
    #data = "the ids of hotels list for each city chosen"
    hotel_entities = {}
    hotels = []
    list1 = []
    k=0
    num_records=0
    for keys in data:
        if keys == "results":
            for result in data[keys]:
                for key1 in result:
                    #print (key1)
                    for vals in result[key1]:
                        ids = result[key1]
                        if vals == 'id':
                            #print (ids[vals])
                            list1.append({'id':ids[vals]})
                            num_records = num_records + 1
                        if vals == 'name':
                            #print (ids[vals])
                            list1.append({'name':ids[vals]})
                    k=k+1
                    hotel_entities[str(k)]=list1
                    list1=[]
    #print ("++hotel_entities++",hotel_entities)

    for item1 in hotel_entities:
    	items = {'ids':str(item1), "id":hotel_entities[item1][0]['id'], "name":hotel_entities[item1][1]['name']}
    	db.hotels.insert(items)


    for num in range(1,num_records):
        output = db.hotels.find_one({"ids":str(num)})
        url="https://api.zomato.com/v1/reviews.json/"+str(output['id'])+"/user?count=5"
        getReviews(url)
        
'''
    for num in range(1,num_records):
    	#print ("++ num ++ ",num)
    	output = db.hotels.find_one({"ids":str(num)})
    	#print (output)
    	#print (output[output['ids']])
    	out2 = output[output['ids']]
    	for hotel_id in out2:
            for keys in hotel_id:
                if keys == 'id':
                    url="https://api.zomato.com/v1/reviews.json/"+str(hotel_id[keys])+"/user?count=5"
                    getReviews(url)
'''