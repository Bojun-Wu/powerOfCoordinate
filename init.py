
def initDb():
    from show_result.models import house
    house.objects.all().delete()
    import csv
    import googlemaps
    with open(r'D:\download\lvr_landcsv\a_lvr_land_a.csv', newline='', encoding="utf-8") as csvfile:
        rows = csv.reader(csvfile)
        count = 0
        for row in rows:
            if '鄉鎮市區' in row[0] or row[0] == 'The villages and towns urban district' or row[22] == '':
                continue
            map_client = googlemaps.Client(
                'AIzaSyAcilcRP58jNHR7JwLyufW6A2zxCL65ePg')
            data = map_client.geocode(row[2])
            if (data == []):
                continue
            house.objects.create(position=row[2], unitPrice=row[22], lat=data[0]['geometry']
                                 ['location']['lat'], lon=data[0]['geometry']['location']['lng'])
            count += 1
            if count > 1000:
                break
