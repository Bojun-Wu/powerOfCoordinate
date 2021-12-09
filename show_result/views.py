from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from init import initDb
from .models import house
import googlemaps
from geopy import distance
from django.views import View

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
    inputDistance = 0

    def get(self, request):
        # for house in self.houseWithin():
        #     print(house.id)
        return render(request, 'show_result/home.html')

    def post(self, request):
        self.inputPosition = request.POST['position']
        self.inputDistance = request.POST['distance']
        map_client = googlemaps.Client(
            'AIzaSyAcilcRP58jNHR7JwLyufW6A2zxCL65ePg')
        data = map_client.geocode(self.inputPosition)
        if data == []:
            return HttpResponse('something went wrong')
        acceptPos = [tempHouse.id for tempHouse in house.objects.all() if calDistance(
            data[0]['geometry']['location']['lat'], data[0]['geometry']['location']['lng'], tempHouse.lat, tempHouse.lon, self.inputDistance)]
        avergePrice = 0
        if len(acceptPos) == 0:
            return render(request, 'show_result/home.html', locals())
        self.houseWithin = house.objects.filter(id__in=acceptPos)
        for price in self.houseWithin:
            avergePrice += price.unitPrice
        avergePrice = round(avergePrice/len(acceptPos))
        return render(request, 'show_result/home.html', locals())
