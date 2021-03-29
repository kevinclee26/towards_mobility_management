import json

# dc_track_id = 'Resources/census.json'

class Polygons:
    def __init__(self, filepath):
        with open(filepath) as f:
            self.polygons = json.load(f)["features"]

    def inside(self, point, vs):
    # Check if the point lies inside a polygon or outside a polygon. Polygon is defined by vs.
    # Return True if inside, otherwise return false
    # point is a list including lat and log
    # vs is a list of list, inner list is a couple lat and lon, which define the edge of the polygon
    # https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
    # https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
        inside = False

        # # x is Lat and y is lon
        x = point[0]
        y = point[1]

        for i in range(len(vs)):
            j = i - 1
            xi = vs[i][0]
            yi = vs[i][1]
            xj = vs[j][0]
            yj = vs[j][1]
            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside

        return inside

    def get_tract_id(self, point):
        tract_ids=[]
        for each_polygon in self.polygons:
            # tract_id = 0

            if self.inside(point, each_polygon["geometry"]["rings"][0]):
                tract_id = each_polygon["attributes"]["TRACTID"]
                # break
                tract_ids.append(tract_id)
        if len(tract_ids)>0: 
            return tract_ids
        else: 
            return 'OOR'
