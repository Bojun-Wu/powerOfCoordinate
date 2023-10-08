from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import house
import googlemaps
from django.views import View
from datetime import datetime, timezone
import requests
import urllib.request
import json
from decouple import config
from utils.utils import calDistance


# Create your views here.
class home_page(View):

    houseWithin = house.objects.all()
    inputPosition = ''
    cleanPosition = ''
    inputDistance = 1000
    googleApiKey = config('GOOGLE_MAP_API_KEY')

    def get(self, request):
        print("got a client")
        return render(request, 'show_result/home.html')

    def post(self, request):
        self.inputPosition = request.POST['position']
        self.inputDistance = request.POST['distance'] if request.POST['distance'] else 1000
        print("got a POST", self.inputPosition, self.inputDistance)

        try:
            self.cleanPosition = self.inputPosition.split(',')
            lat = float(self.cleanPosition[0])
            lng = float(self.cleanPosition[1])
            displayLocation = [['current position', lat, lng]]

        except:
            map_client = googlemaps.Client(self.googleApiKey)
            try:
                data = map_client.geocode(self.inputPosition)
            except:
                data = []
            if data == []:
                return render(request, 'show_result/home.html')
            lat = data[0]['geometry']['location']['lat']
            lng = data[0]['geometry']['location']['lng']
            displayLocation = [[self.inputPosition, lat, lng]]

        acceptPos = [tempHouse.id for tempHouse in house.objects.all() if calDistance(
            lat, lng, tempHouse.lat, tempHouse.lon, self.inputDistance)]
        avergePrice = 0
        if len(acceptPos) == 0:
            return render(request, 'show_result/showResult.html', locals())
        
        self.houseWithin = house.objects.filter(id__in=acceptPos)
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
