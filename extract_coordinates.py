import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

# قراءة الملف
file = "احصاء 26.xlsx"

df = pd.read_excel(file)

geolocator = Nominatim(user_agent="aswan_schools")

latitudes = []
longitudes = []

for index,row in df.iterrows():

    address = str(row['اسم المدرسة']) + " " + str(row['الموقع']) + " اسوان مصر"

    try:
        location = geolocator.geocode(address)

        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append("")
            longitudes.append("")

    except:
        latitudes.append("")
        longitudes.append("")

    sleep(1)

df['latitude'] = latitudes
df['longitude'] = longitudes

df.to_excel("schools_coordinates.xlsx",index=False)

print("تم استخراج الإحداثيات")