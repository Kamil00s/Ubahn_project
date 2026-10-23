from geopy.distance import geodesic
    def find_closest_n(graph,lat,lon,max=3):
        #find closest n stations to lat lon
        all={}
        res ={}
        
        for node in graph:
            dist = geodesic((lat,lon),(graph[node][0]["from_lat"],graph[node][0]["from_lon"])).meters
            if node not in all:
                all[node] = dist

        sorted_nodes = sorted(all.items(), key=lambda x: x[1])
        for node, dist in sorted_nodes[:max]:
            res[node] = dist
        print(f"Closest {max} stations to {lat},{lon}: {res}")
        return res