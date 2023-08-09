import csv
import json
import sys
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radius of the Earth in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2) * math.sin(d_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def main():
    if len(sys.argv) != 3:
        print("Usage: geo-cmp.py geo_cat.csv address.json")
        return

    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        geo_cat_data = list(reader)

    with open(sys.argv[2], 'r') as f:
        address_data = json.load(f)

    if len(address_data) != 2 * len(geo_cat_data):
        print("Error: The number of entries in address.json is not double the number of entries in geo_cat.csv")
        return

    with open('geo_cmp.csv', 'w') as f:
        writer = csv.writer(f)
        for i in range(len(geo_cat_data)):
            lat1 = address_data[2*i]['lat']
            lon1 = address_data[2*i]['lon']
            lat2 = address_data[2*i+1]['lat']
            lon2 = address_data[2*i+1]['lon']

            distance = haversine(lat1, lon1, lat2, lon2)
            writer.writerow([geo_cat_data[i][0], distance, geo_cat_data[i][1], geo_cat_data[i][2]])

if __name__ == "__main__":
    main()
