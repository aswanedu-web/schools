import pandas as pd
from geopy.geocoders import Nominatim
import time

# 1. إعداد أداة تحديد المواقع (User_agent يمكن أن يكون أي اسم)
geolocator = Nominatim(user_agent="aswan_schools_locator")

# 2. قراءة البيانات من الملف النصي (تأكد أن الملف في نفس المجلد)
file_path = 'احصاء 26.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    schools_list = f.readlines()

data = []

print("جاري استخراج الإحداثيات... يرجى الانتظار")

for school in schools_list:
    school_name = school.strip()
    if not school_name: continue
    
    try:
        # البحث عن المدرسة في نطاق محافظة أسوان لزيادة الدقة
        location = geolocator.geocode(f"{school_name}, Aswan, Egypt")
        
        if location:
            data.append({
                'اسم المدرسة': school_name,
                'العنوان الكامل': location.address,
                'Latitude': location.latitude,
                'Longitude': location.longitude
            })
        else:
            # في حال لم يجد الموقع الدقيق، يضع علامة للمراجعة
            data.append({
                'اسم المدرسة': school_name,
                'العنوان الكامل': "تحتاج مراجعة يدويًا",
                'Latitude': None,
                'Longitude': None
            })
        
        # تأخير بسيط لتجنب حظر الخدمة (API Rate Limit)
        time.sleep(1) 
        
    except Exception as e:
        print(f"خطأ في معالجة {school_name}: {e}")

# 3. تحويل النتائج إلى ملف Excel
df = pd.DataFrame(data)
df.to_excel('احداثيات_مدارس_اسوان_2026.xlsx', index=False)

print("تم بنجاح! تم إنشاء ملف: احداثيات_مدارس_اسوان_2026.xlsx")
