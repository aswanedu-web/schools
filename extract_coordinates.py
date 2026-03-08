import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
from io import BytesIO

# إعداد الصفحة لتناسب واجهة مديرية التربية والتعليم بأسوان
st.set_page_config(page_title="منظومة إحداثيات مدارس أسوان", page_icon="📍")

st.title("📍 نظام استخراج الإحداثيات الجغرافية")
st.markdown("### خاص ببيانات إحصاء مدارس محافظة أسوان 2026")
st.info("دكتور / ربيع أبو يوسف - إدارة التحول الرقمي")

# رفع ملف الإحصاء (txt)
uploaded_file = st.file_uploader("اختر ملف (احصاء 26.txt)", type=['txt'])

if uploaded_file:
    # قراءة وتنظيف قائمة المدارس
    raw_data = uploaded_file.read().decode("utf-8")
    schools = [s.strip() for s in raw_data.split('\n') if s.strip()]
    
    st.write(f"📊 تم اكتشاف عدد ({len(schools)}) مدرسة في الملف.")
    
    if st.button("🚀 بدء المعالجة وإنشاء ملف Excel"):
        # إعداد المحرك مع مهلة زمنية أطول لتجنب الأخطاء
        geolocator = Nominatim(user_agent="aswan_edu_mapper_2026", timeout=10)
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)
        
        results = []
        progress_bar = st.progress(0)
        
        for idx, school in enumerate(schools):
            # البحث عن المدرسة في نطاق أسوان تحديداً
            try:
                location = geocode(f"{school}, Aswan, Egypt")
                if location:
                    results.append({
                        "اسم المدرسة": school,
                        "العنوان": location.address,
                        "Latitude": location.latitude,
                        "Longitude": location.longitude
                    })
                else:
                    results.append({"اسم المدرسة": school, "العنوان": "غير موجود بالخرائط", "Latitude": None, "Longitude": None})
            except:
                results.append({"اسم المدرسة": school, "العنوان": "خطأ تقني", "Latitude": None, "Longitude": None})
            
            # تحديث شريط التقدم
            progress_bar.progress((idx + 1) / len(schools))
        
        # عرض النتائج في جدول
        df = pd.DataFrame(results)
        st.success("✅ اكتملت العملية!")
        st.dataframe(df)

        # تحويل البيانات إلى Excel للتحميل الفوري
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='المدارس')
        
        st.download_button(
            label="📥 تحميل ملف Excel الجاهز",
            data=output.getvalue(),
            file_name="احداثيات_مدارس_اسوان_2026.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
