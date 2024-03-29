from django.core.management.base import BaseCommand
import time
from show_result.models import house
import csv
import googlemaps
from datetime import datetime
from decouple import config

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        googleApiKey = config('GOOGLE_MAP_API_KEY')
        file = "static/taipei.csv"
        with open(file, newline='', encoding="utf-8") as csvfile:
            rows = csv.reader(csvfile)
            count = 0
            for row in rows:
                # # d_a
                # if(count >= 8000):
                #     break

                if '鄉鎮市區' in row[0] or row[0] == 'The villages and towns urban district' or (not row[22]) or (not int(row[22])) or row[26] != '' or row[1] == '土地' or row[1] == '車位':
                    continue
                count += 1
                map_client = googlemaps.Client(googleApiKey)
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
                print(f"Got building No.{count}")
                time.sleep(1)