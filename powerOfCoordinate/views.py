from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from init import initDb
import io


# def setting(request):
#     initDb()
#     return HttpResponseRedirect('/show_result/home')


def setting(request):
    if request.method == 'GET':
        return render(request, 'setting.html')
    elif request.method == 'POST':
        from show_result.models import house
        house.objects.all().delete()
        import csv
        import googlemaps
        from datetime import datetime
        request.upload_handlers.pop(0)
        file = request.FILES['file'].file.name
    with open(file, newline='', encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile)
        count = 0
        for row in rows:
            # count += 1
            # if(count >= 9000):
            #     break
            if '鄉鎮市區' in row[0] or row[0] == 'The villages and towns urban district' or row[22] == '' or row[26] != '' or row[1] == '土地' or row[1] == '車位':
                continue
            map_client = googlemaps.Client(
                'AIzaSyAcilcRP58jNHR7JwLyufW6A2zxCL65ePg')
            data = map_client.geocode(row[0]+row[2])
            if (data == []):
                continue
            if(row[14] != ''):
                if(int(row[14][:-4]) < 200 and int(row[14][:-4]) > 0):
                    houseAge = datetime.now().year-(int(row[14][:-4])+1911)
            else:
                houseAge = None
            if('車位' in row[1]):
                sellType = '建土車'
            elif('土地' in row[1]):
                sellType = '建土'
            else:
                sellType = '建'
            house.objects.create(position=row[2], unitPrice=row[22], lat=data[0]['geometry']
                                 ['location']['lat'], lon=data[0]['geometry']['location']['lng'], age=houseAge, building_state=row[11][:2], transaction_sign=sellType)
            count += 1
            if count > int(request.POST['amount']):
                break
    return HttpResponseRedirect('/')
