import requests
import pymongo
import time
import secrets
from geo_polygons import Polygons # Polygons holds the locality shapes
import sys
from Resources.companies import compInfo # compInfo contains info about companies

dc_track_id_path = 'Resources/census.json'
# URL = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/152/query?where=1%3D1&outFields=OBJECTID,AIRTEMP,RELATIVEHUMIDITY,VISIBILITY,WINDSPEED,DATADATETIME&outSR=4326&f=json'
census_polygons=Polygons(dc_track_id_path)


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.scooters_DB
weather_docs=db.weather_docs
scooter_docs=db.scooter_docs
log=db.log

def get_bike_data(company_info):
    name=company_info['name']
    jobname=secrets.token_urlsafe(16)
    try:
        response = requests.get(company_info["url"])
        response_json=response.json()
        try: 
            last_updated=response_json['last_updated']
        except: 
            last_updated='NA'
        data=response_json
        for each_layer in company_info["layers"]:
            data = data[each_layer]
        for each_feature in data: 
            each_feature['jobname']=jobname
        scooter_docs.insert_many(data)
        log.insert_one({'time': time.time(), 
                        'jobname': jobname, 
                        'last_updated': last_updated, 
                        'len': len(data), 
                        'status': 'success', 
                        'name': name, 
                        'size': sys.getsizeof(data)})
    except:
        # If a company url doesn't work, continue next company url, print the url that is not work
        print(f"{name} url has issue")
        log.insert_one({'time': time.time(), 
                        'jobname': jobname, 
                        'name': name, 
                        'len': 0, 
                        'size': 0, 
                        'last_updated': 'NA', 
                        'status': 'failed'}) 
    return 'complete'

def all_scooter_data(): 
    for each_company in compInfo: 
        print(each_company['name']+'-'+get_bike_data(each_company))
    # print(one_company)
    return 'compete'

def weather_data():
    weather_url='https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/152/query?where=1%3D1&outFields=OBJECTID,AIRTEMP,RELATIVEHUMIDITY,VISIBILITY,WINDSPEED,DATADATETIME&outSR=4326&f=json'
    jobname=secrets.token_urlsafe(16)
    try: 
        response = requests.get(weather_url)
        response_json = response.json()
        data=response_json['features']
        try: 
            last_updated=response_json['last_updated']
        except: 
            last_updated='NA'
        for each_feature in data: 
            each_feature['jobname']=jobname
        weather_docs.insert_many(data)            
        log.insert_one({'time': time.time(), 
                        'jobname': jobname, 
                        'last_updated': last_updated, 
                        'len': len(data), 
                        'status': 'success', 
                        'name': 'weather', 
                        'size': sys.getsizeof(data)})  
    except:
        # If a company url doesn't work, continue next company url, print the url that is not work
        print("weather url has issue")
        log.insert_one({'time': time.time(), 
                        'jobname': jobname, 
                        'len': 0, 
                        'size': 0, 
                        'last_updated': 'NA', 
                        'name': weather, 
                        'status': 'failed'}) 
    return 'complete'
    # weather_data=[each_feature['jobname']=jobname for each_feature in weather_data]
    # doc_sets = process_weather_data(weather_data)


    # Save "doc_sets" to MongoDB
    # collection.insert_one({'data': doc_sets})
    # collection.insert_many(doc_sets)
    # if doc_sets: 
    #     return True
    # else: 
    #     return False
    # return len(data), sys.getsizeof(data)

# def scooter_data(jobname=str(round(time.time(), 0))):
#     all_data=[]
#     for each_company in compInfo:
#         name=each_company["name"]
#         # print("$$$ ", name)
#         try:
#             response = requests.get(each_company["url"])
#             data=response.json()
#         except:
#             # If a company url doesn't work, continue next company url, print the url that is not work
#             print(f"{name} url has issue")
#             continue
#         # Assign the value of last_updated to varialbe "last_updated"
#         # if data doesn't have last_updated attibute, use current time as "last_updated"
#         # Make sure the last_updated is integer for future use
#         # try:
#         #     last_updated = int(data["last_updated"])
#         # except:
#         #     # 🍎Issue, using current time would save much more records, need modify later
#         #     last_updated = int(time.time())

#         # Retrieve data by layers
#         for each_layer in each_company["layers"]:
#             data = data[each_layer]
#         for each_feature in data: 
#             each_feature['jobname']=jobname
#             each_feature['name']=name
#         all_data=all_data+data
#     scooter_docs.insert_many(all_data)
#     return len(all_data), sys.getsizeof(all_data)

#         # If last_updated changes, save data to mongoDB
        # if last_updated > recent_last_updated[name]:
            # Process data and save data to MongoDB
            # doc_sets = process_data(data, name, last_updated)
            # collection.insert_many(doc_sets)

        # update recent_last_updated
        # recent_last_updated[name] = last_updated

# def process_weather_data(data): 
#     doc_sets = []
#     for each_record in data:
#         lat = float(each_record["geometry"]["y"])
#         lon = float(each_record["geometry"]["x"])
#         point = [lon, lat]
#         tractid = census_polygons.get_tract_id(point)

#         new_doc = {}
#         new_doc["air_temp"] = each_record["attributes"]["AIRTEMP"]
#         new_doc["humidity"] = each_record["attributes"]["RELATIVEHUMIDITY"]
#         new_doc["visibility"] = each_record["attributes"]["VISIBILITY"]
#         new_doc["wind_speed"] = each_record["attributes"]["WINDSPEED"]
#         new_doc["last_updated"] = int(int(each_record["attributes"]["DATADATETIME"]) / 1000)
#         new_doc["tractid"] = tractid
#         # new_doc["saved_at"] = int(time.time())

#         doc_sets.append(new_doc)
#     return doc_sets

# def process_weather_data(data):
#     polygons = Polygons()
#     doc_sets = []
#     for each_record in data:
#         lat = float(each_record["geometry"]["y"])
#         lon = float(each_record["geometry"]["x"])
#         point = [lon, lat]
#         tractid = polygons.get_tractid(point)

#         new_doc = {}
#         new_doc["air_temp"] = each_record["attributes"]["AIRTEMP"]
#         new_doc["humidity"] = each_record["attributes"]["RELATIVEHUMIDITY"]
#         new_doc["visibility"] = each_record["attributes"]["VISIBILITY"]
#         new_doc["wind_speed"] = each_record["attributes"]["WINDSPEED"]
#         new_doc["last_updated"] = int(int(each_record["attributes"]["DATADATETIME"]) / 1000)
#         new_doc["tractid"] = tractid
#         new_doc["saved_at"] = int(time.time())

#         doc_sets.append(new_doc)

#     return doc_sets



  
