import requests
import pymongo
import time
import secrets
# from geo_polygons import Polygons # Polygons holds the locality shapes
import sys
from Resources.companies import compInfo # compInfo contains info about companies
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# dc_track_id_path = 'Resources/census.json'
# URL = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/152/query?where=1%3D1&outFields=OBJECTID,AIRTEMP,RELATIVEHUMIDITY,VISIBILITY,WINDSPEED,DATADATETIME&outSR=4326&f=json'
# census_polygons=Polygons(dc_track_id_path)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.scooters_DB
weather_docs=db.weather_docs
scooter_docs=db.scooter_docs
log=db.log

# Initialize SQLAlchemy to work with Postgres
conn = 'postgresql://postgres:postgres@localhost:5432/scooters_DB'
engine=sqlalchemy.create_engine(conn)

# Define database and collection
Base=automap_base()
Base.prepare(engine, reflect=True)
Completed_log=Base.classes.completed_log
Current_fleet=Base.classes.current_fleet
Removed=Base.classes.removed

def get_bike_data(company_info):
    name=company_info['name']
    jobname=secrets.token_urlsafe(16)
    last_updated=time.time()
    try:
        response = requests.get(company_info["url"])
        response_json=response.json()
        try: 
            last_updated=response_json['last_updated']
        except: 
            pass
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
                        'processed': False, 
                        'size': sys.getsizeof(data)})
    except:
        # If a company url doesn't work, continue next company url, print the url that is not work
        # print(f"{name} url has issue")
        log.insert_one({'time': time.time(), 
                        'jobname': jobname, 
                        'name': name, 
                        'len': 0, 
                        'size': 0, 
                        'processed': False, 
                        'last_updated': last_updated, 
                        'status': 'failed'}) 
    return 'complete'

def all_scooter_data(): 
    for each_company in compInfo: 
        # if each_company['hash']==False: 
        get_bike_data(each_company)
        # print(each_company['name']+'-'+get_bike_data(each_company))
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
            last_updated=time.time()
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
        # print("weather url has issue")
        log.insert_one({'time': time.time(), 
                        'jobname': jobname, 
                        'len': 0, 
                        'size': 0, 
                        'last_updated': 'NA', 
                        'name': weather, 
                        'status': 'failed'}) 
    return 'complete'
  
def new_log_params(job_log): 
    record_params={'time': job_log['time'], 
         'jobname': job_log['jobname'], 
         'last_updated': job_log['last_updated'], 
         'len': job_log['len'], 
         'status': job_log['status'], 
         'name': job_log['name'], 
         'size': job_log['size'], 
         'processed_time': time.time(), 
         'processed': True}
    return record_params

def update_existing_params(scooter, job_log): 
    record_params={'path': scooter['path']+(scooter['lat'], scooter['lon']), 
                   'lon': scooter['lon'], 
                   'lat': scooter['lat'],
                   'last_updated': job_log['last_updated'], 
                   'is_reserved': scooter.get('is_reserved', None), 
                   'is_disabled': scooter.get('is_disabled', None), 
                   'battery_level': scooter.get('battery_level', None), 
                   'jobname': job_log['jobname'], 
                   'new': False}
    return record_params

def new_scooter_params(scooter, job_log): 
    record_params={'start_time': job_log['last_updated'], 
                   'path': (scooter['lat'], scooter['lon']), 
                   'bike_id': scooter['bike_id'], 
                   'company_name': job_log['name'], 
                   'start_is_reserved': scooter.get('is_reserved', None), 
                   'start_is_disabled': scooter.get('is_disabled', None), 
                   'start_battery_level': scooter.get('battery_level', None), 
                   'lon': scooter['lon'], 
                   'lat': scooter['lat'], 
                   'is_reserved': scooter.get('is_reserved', None),
                   'is_disabled': scooter.get('is_disabled', None), 
                   'battery_level': scooter.get('battery_level', None), 
                   'last_updated': job_log['last_updated'], 
                   'jobname': job_log['jobname'], #each_scooter['jobname'], 
                   'new': True}
    return record_params

def process_job(job): 
    session=Session(engine)
    # find scooter record from Mongo
    scooters_list=list(scooter_docs.find({'jobname': job['jobname']}))

    # get list of current fleet from Postgres
    current_fleet_list=session.query(Current_fleet).filter(Current_fleet.company_name==job['name']).all()
    current_fleet_id_list=[scooter.bike_id for scooter in current_fleet_list]
    fleet_list=current_fleet_id_list.copy()

    # work on current
    for each_scooter in scooters_list: 
        current_id=each_scooter['bike_id']
        current_index=current_fleet_id_list.index(current_id) if current_id in current_fleet_id_list else None
        if not current_index==None: # if found then edit attributes  
            scooter_rec=current_fleet_list[current_index] 
            fleet_list.remove(current_id) # remove
            scooter_params=update_existing_params(each_scooter, job)
            for key, value in scooter_params.items(): 
                setattr(scooter_rec, key, value)
        else: # else new bike
            scooter_params=new_scooter_params(each_scooter, job)
            session.add(Current_fleet(**scooter_params))

    # work on removed - get list of to be removed
    removed_table_columns=sqlalchemy.inspect(Current_fleet).columns.keys()
    remaining_fleet=session.query(Current_fleet).filter(Current_fleet.company_name==job['name']).filter(Current_fleet.bike_id.in_(fleet_list)).all()
    for each_move_data in remaining_fleet: # iterate through left over
        session.add(Removed(**{column: each_move_data.__dict__[column] for column in removed_table_columns}))
        session.delete(each_move_data)

    # process job
    log_params=new_log_params(job)
    session.add(Completed_log(**log_params))
    session.commit()
    
    # update Mongo
    log.remove({'_id': job['_id']})
    scooter_docs.remove({'jobname': job['jobname']})

    session.close()
    return 'complete'

def process_log():
    all_jobs=list(log.find())
    sorted_log=sorted(all_jobs, key=lambda log: log['time'])
    for each_job in sorted_log: 
        process_job(each_job)
    return 'complete'