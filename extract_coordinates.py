import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import time
from io import BytesIO

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستخرج إحداثيات مدارس أسوان 2026", layout="wide")
st.title("📍 مستخرج إحداثيات المدارس (إحصاء 2026)")
st.subheader("دكتور / ربيع أبو يوسف - مديرية التربية والتعليم بأسوان")

# رفع الملف
uploaded_file = st.file_uploader("قم برفع ملف (احصاء 26.txt)", type=['txt'])

if uploaded_file is not None:
    # قراءة الأسماء من الملف المرفوع
    content = uploaded_file.read().decode("utf-8")
    schools_list = [line.strip() for line in content.split('\n') if line.strip()]
    
    if st.button("بدء استخراج الإحداثيات (Excel)"):
        geolocator = Nominatim(user_agent="aswan_schools_app_2026")
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, school in enumerate(schools_list):
            status_text.text(f"جاري معالجة: {school} ({i+1}/{len(schools_list)})")
            try:
                # البحث في نطاق أسوان لضمان الدقة
                location = geolocator.geocode(f"{school}, Aswan, Egypt")
                if location:
                    results.append({
                        'اسم المدرسة': school,
                        'العنوان': location.address,
                        'Latitude': location.latitude,
                        'Longitude': location.longitude
                    })
                else:
                    results.append({'اسم المدرسة': school, 'العنوان': 'غير محدد', 'Latitude': None, 'Longitude': None})
                
                time.sleep(1.1) # لتجنب حظر السيرفر
            except:
                results.append({'اسم المدرسة': school, 'العنوان': 'خطأ في الاتصال', 'Latitude': None, 'Longitude': None})
            
            progress_bar.progress((i + 1) / len(schools_list))

        # تحويل النتائج إلى DataFrame
        df = pd.DataFrame(results)
        st.success("✅ تمت المعالجة بنجاح!")
        st.dataframe(df)

        # تحويل DataFrame إلى ملف Excel في الذاكرة للتحميل
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        st.download_button(
            label="📥 تحميل ملف Excel الناتج",
            data=output.getvalue(),
            file_name="احداثيات_مدارس_اسوان_2026.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
