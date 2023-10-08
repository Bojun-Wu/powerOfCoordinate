from geopy import distance

def calDistance(pointAlat, pointAlon, pointBlat, pointBlon, inputDistance):
    pointA = (pointAlat, pointAlon)
    pointB = (pointBlat, pointBlon)
    if ((distance.distance(pointA, pointB).km)*1000 > float(inputDistance)):
        return False
    else:
        return True