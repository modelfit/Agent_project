import requests
from datetime import datetime

def _get_location_ip() -> tuple[str,str]:
    """
    Detects city and country from current IP address.
    Returns (city, country) or falls back to Riyadh, Saudi Arabia.
    """
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data['status'] ==  "success":
            return data['city'], data['country']
    except:
        pass
    return "Riyadh", "Saudi Arabia"

def get_prayer_times(city: str, country: str = ""):
    """
    يجلب مواقيت الصلاة تلقائياً بناءً على موقعك الحالي من عنوان IP.
    يمكن تحديد المدينة يدوياً إذا أردت مدينة مختلفة.

    Args:
        city: اسم المدينة بالإنجليزية (اختياري — يُكتشف تلقائياً إذا لم يُحدد)
        country: اسم الدولة بالإنجليزية (اختياري — يُكتشف تلقائياً إذا لم يُحدد)
    """
    try:
        if not city or not country:
            detected_city, detected_country = _get_location_ip()
            city = city or detected_city
            country = country or detected_country

        today = datetime.now().strftime("%d-%m-%Y")

        response = requests.get(
            "https://api.aladhan.com/v1/timingsByCity",
            params={
                "city":    city,
                "country": country,
                "method":  4,
                "date":    today,
            },
            timeout=10,
        )
        if response.status_code != 200:
            return f"خطأ في جلب مواقيت الصلاة: {response.status_code}"
        
        data    = response.json()["data"]["timings"]
        hijri   = response.json()["data"]["date"]["hijri"]
        gregori = response.json()["data"]["date"]["gregorian"]

        hijri_months = [
            "محرم", "صفر", "ربيع الأول", "ربيع الثاني",
            "جمادى الأولى", "جمادى الثانية", "رجب", "شعبان",
            "رمضان", "شوال", "ذو القعدة", "ذو الحجة"
        ]

        hijri_month = hijri_months[int(hijri["month"]["number"]) - 1]
        hijri_date  = f"{hijri['day']} {hijri_month} {hijri['year']} هـ"
        greg_date   = f"{gregori['day']} {gregori['month']['en']} {gregori['year']} م"

        return f""" مواقيت الصلاة في {city}، {country}
                 {greg_date} | {hijri_date}

                 الفجر:    {data['Fajr']}
                 الشروق:   {data['Sunrise']}
                 الظهر:    {data['Dhuhr']}
                 العصر:    {data['Asr']}
                 المغرب:   {data['Maghrib']}
                 العشاء:   {data['Isha']}

                📍 تم اكتشاف الموقع تلقائياً من عنوان IP"""
    except requests.exceptions.Timeout:
        return "خطأ: انتهت مهلة الاتصال بالخادم."
    except requests.exceptions.ConnectionError:
        return "خطأ: تعذّر الاتصال بالإنترنت."
    except Exception as e:
        return f"خطأ في جلب مواقيت الصلاة: {str(e)}"