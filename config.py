# config.py

# ضع توكن البوت الخاص بك هنا (تحصل عليه من BotFather)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# قائمة الولايات المطلوبة (ولاية حضرموت + 20 ولاية جزائرية)
LOCATIONS = {
    "ولاية حضرموت": {"city": "Hadramaut", "country": "Yemen"},
    "ولاية الجزائر": {"city": "Algiers", "country": "Algeria"},
    "ولاية وهران": {"city": "Oran", "country": "Algeria"},
    "ولاية قسنطينة": {"city": "Constantine", "country": "Algeria"},
    "ولاية عنابة": {"city": "Annaba", "country": "Algeria"},
    "ولاية البليدة": {"city": "Blida", "country": "Algeria"},
    "ولاية سطيف": {"city": "Setif", "country": "Algeria"},
    "ولاية باتنة": {"city": "Batna", "country": "Algeria"},
    "ولاية الجلفة": {"city": "Djelfa", "country": "Algeria"},
    "ولاية بسكرة": {"city": "Biskra", "country": "Algeria"},
    "ولاية تلمسان": {"city": "Tlemcen", "country": "Algeria"},
    "ولاية تبسة": {"city": "Tebessa", "country": "Algeria"},
    "ولاية بجاية": {"city": "Bejaia", "country": "Algeria"},
    "ولاية سكيكدة": {"city": "Skikda", "country": "Algeria"},
    "ولاية جيجل": {"city": "Jijel", "country": "Algeria"},
    "ولاية مستغانم": {"city": "Mostaganem", "country": "Algeria"},
    "ولاية المسيلة": {"city": "M'Sila", "country": "Algeria"},
    "ولاية الشلف": {"city": "Chlef", "country": "Algeria"},
    "ولاية سيدي بلعباس": {"city": "Sidi Bel Abbes", "country": "Algeria"},
    "ولاية مدية": {"city": "Medea", "country": "Algeria"},
    "ولاية ورقلة": {"city": "Ouargla", "country": "Algeria"},
}

# قاعدة بيانات تجريبية للأحداث الإسلامية حسب اليوم والشهر الهجري (صيغة: "الشهر-اليوم")
ISLAMIC_EVENTS = {
    "01-01": "رأس السنة الهجرية (هجرة النبي صلى الله عليه وسلم).",
    "01-10": "يوم عاشوراء (نجاة سيدنا موسى عليه السلام).",
    "03-12": "المولد النبوي الشريف على صاحبها أفضل الصلاة والسلام.",
    "09-01": "أول أيام شهر رمضان المبارك (بدء الصيام).",
    "09-17": "غزوة بدر الكبرى (الفرقان).",
    "09-20": "فتح مكة المكرمة.",
    "10-01": "عيد الفطر المبارك.",
    "12-09": "يوم عرفة (الحج الأكبر).",
    "12-10": "عيد الأضحى المبارك.",
}

