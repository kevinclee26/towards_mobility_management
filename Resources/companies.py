# Updated on 3/26/21
# https://ddot.dc.gov/page/dockless-api
compInfo = [
  # {
  #   "name": 'lyft', 
  #   # can rehash
  #   # "url": '/assets/data/lyft',//.json',
  #   "url":
  #     'https://s3.amazonaws.com/lyft-lastmile-production-iad/lbs/dca/free_bike_status.json',
  #   "permit": 1020,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'],
  #   "hash": True
  # },
  # {
  #   "name": 'lime', 
  #   # //can rehash
  #   # "url": '/assets/data/lime',//.json',
  #   "url":
  #     'https://data.lime.bike/api/partners/v1/gbfs/washington_dc/free_bike_status.json',
  #   "permit": 720,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'], 
  #   "hash": True
  # },
  {
    "name": 'spin',
    # "url": '/assets/data/spin',//.json',
    "url": 'https://web.spin.pm/api/gbfs/v1/washington_dc/free_bike_status',
    "permit": 1720,
    "proxy": False,
    "layers": ['data', 'bikes'],
    "hash": False
  },
  # {
  #   "name": 'skip',
  #   # "url": '/assets/data/skip',//.json',
  #   "url": 'https://us-central1-waybots-production.cloudfunctions.net/ddotApi-dcFreeBikeStatus',
  #   "permit": 2500,
  #   "proxy": True,
  #   "layers": ['bikes'],
  #   "hash": True
  # },
  # {
  #   "name": 'bird', #//can rehash
  #   # "url": '/assets/data/bird',//.json',
  #   "url": 'https://gbfs.bird.co/dc',
  #   "permit": 720,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'],
  #   "hash": True
  # },
  # {
  #   "name": 'razor',
  #   # "url": '/assets/data/razor',//.json',
  #   "url": 'https://razorapi.net/api/v1/gbfs/Washington%20DC/free_bike_status.json',
  #   "permit": 720,
  #   "proxy": True,
  #   "layers": ['data', 'bikes'],
  #   "hash": True
  # }, 
  # {
  #   "name": 'helbiz',
  #   "url": 'https://api.helbiz.com/admin/reporting/washington/gbfs/free_bike_status.json',
  #   "permit": 0,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'],
  #   "hash": True
  # }, 
  # {
  #   "name": 'capitalbikeshare',
  #   "url": 'https://gbfs.capitalbikeshare.com/gbfs/en/free_bike_status.json',
  #   "permit": 0,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'],
  #   "hash": True
  # }, 
  # {
  #   "name": 'bolt',
  #   "url": 'https://api-lb.micromobility.com/dc/gbfs/en/free_bike_status.json',
  #   "permit": 0,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'],
  #   "hash": True
  # }, 
  # JUMP and LIME uses the same? 
  # {
  #   "name": 'jump',
  #   # "url": '/assets/data/razor',//.json',
  #   "url": 'https://data.lime.bike/api/partners/v1/gbfs/washington_dc/free_bike_status',
  #   "permit": 0,
  #   "proxy": False,
  #   "layers": ['data', 'bikes'],
  # }
]

