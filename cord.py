from geopy.distance import geodesic
def find_closest(graph,lat,lon):
    #find closest station, return sorted list of stations with distance
    all={}
    res ={}
        
    for node in graph:
        dist = geodesic((lat,lon),(graph[node][0]["from_lat"],graph[node][0]["from_lon"])).meters
        if node not in all:
            all[node] = dist

    sorted_nodes = sorted(all.items(), key=lambda x: x[1])
    for node, dist in sorted_nodes:
        res[node] = dist
    return res
    
def how_many_meters(lat1,lon1,lat2,lon2):
    #find distance between two points
    dist = geodesic((lat1,lon1),(lat2,lon2)).meters
    print(f"Distance between {lat1},{lon1} and {lat2},{lon2}: {dist} meters")
    return dist

