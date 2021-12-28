from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from init import initDb
from .models import house
import googlemaps
from geopy import distance
from django.views import View
from datetime import datetime, timezone
import requests
import urllib.request
import json

# Create your views here.


def calDistance(pointAlat, pointAlon, pointBlat, pointBlon, inputDistance):
    pointA = (pointAlat, pointAlon)
    pointB = (pointBlat, pointBlon)
    if ((distance.distance(pointA, pointB).km)*1000 > float(inputDistance)):
        return False
    else:
        return True


# def home(request):

#     if request.method == 'GET':
#         for i in houseWithin:
#             print(i.id)
#         return render(request, 'show_result/home.html', locals())

#     elif request.method == "POST":
#         inputPosition = request.POST['position']
#         inputDistance = request.POST['distance']
#         with urllib.request.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+urllib.parse.quote(inputPosition)+"&key=AIzaSyAcilcRP58jNHR7JwLyufW6A2zxCL65ePg") as url:
#             data = json.loads(url.read().decode())
#             acceptPos = [house.id for house in house.objects.all() if calDistance(data['results'][0]['geometry']["location"]
#                                                                                   ['lat'], data['results'][0]['geometry']["location"]['lng'], house.lat, house.lon, inputDistance)]
#             print(acceptPos)
#             houseWithin = house.objects.filter(id__in=acceptPos)
#         return HttpResponseRedirect('/show_result/home')


class home_page(View):

    houseWithin = house.objects.all()
    inputPosition = ''
    inputDistance = 1000

    def get(self, request):
        return render(request, 'show_result/home.html')

    def post(self, request):
        self.inputPosition = request.POST['position']
        self.inputDistance = request.POST['distance']
        if(self.inputDistance == ''):
            self.inputDistance = 1000
        if(self.inputPosition == 'Current Position'):
            response = requests.post(
                "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDowkWVDSteeMLzGZfRoPgrCiXGnx2_lkk")
            lat = json.loads(response.content)['location']['lat']
            lng = json.loads(response.content)['location']['lng']
        else:
            map_client = googlemaps.Client(
                'AIzaSyAcilcRP58jNHR7JwLyufW6A2zxCL65ePg')
            data = map_client.geocode(self.inputPosition)
            if data == []:
                return HttpResponse('something went wrong')
            lat = data[0]['geometry']['location']['lat']
            lng = data[0]['geometry']['location']['lng']
        acceptPos = [tempHouse.id for tempHouse in house.objects.all() if calDistance(
            lat, lng, tempHouse.lat, tempHouse.lon, self.inputDistance)]
        avergePrice = 0
        if len(acceptPos) == 0:
            return render(request, 'show_result/showResult.html', locals())
        self.houseWithin = house.objects.filter(id__in=acceptPos)
        displayLocation = [[self.inputPosition, lat, lng]]
        loopcount = 0
        for tempHouse in self.houseWithin:
            loopcount += 1
            tempHouse.TWprice = "${:,.2f}".format(tempHouse.unitPrice*3.30579)
            avergePrice += tempHouse.unitPrice
            tempHouse.last_update = (
                datetime.now(timezone.utc)-tempHouse.update_time).days
            displayLocation.append(
                [str(loopcount)+". "+tempHouse.position, tempHouse.lat, tempHouse.lon])
            tempHouse.id = loopcount
        displayLocationPass = str(displayLocation)
        avergePrice = "{:,.2f}".format(
            round(avergePrice/len(acceptPos)*3.30579, 2))
        return render(request, 'show_result/showResult.html', locals())
