import os
import logging
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات لتتبع الأخطاء في منصة ريلواي
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# قراءة التوكن تلقائياً من خانة الـ Variables في ريلواي
BOT_TOKEN = os.getenv("BOT_TOKEN")

# قائمة الولايات (ولاية حضرموت + 20 ولاية جزائرية)
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

# قاعدة بيانات الأحداث الإسلامية بالتاريخ الهجري (صيغة: "الشهر-اليوم")
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

# الأزرار المتواجدة داخل حقل الكتابة
def get_main_keyboard():
    keyboard = [
        ["🕌 مواقيت الصلاة", "📆 التقويم الهجري"],
        ["📜 أحداث تاريخية", "⚙️ ضبط الولاية"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, placeholder="اختر من القائمة أدناه...")

# دالة الترحيب عند إرسال /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"أهلاً وسهلاً بك يا {user_name} في البوت الإسلامي الشامل.\n\n"
        "يسعدني تقديم خدمات التذكير بمواقيت الصلاة، التاريخ الهجري، والأحداث الإسلامية."
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# دالة جلب البيانات الإسلامية والمواقيت من API
def get_islamic_data(city, country):
    try:
        url = f"https://aladhan.com{city}&country={country}&method=1"
        response = requests.get(url).json()
        if response['code'] == 200:
            return response['data']
    except Exception as e:
        logging.error(f"Error fetching data from API: {e}")
    return None

# دالة معالجة الرسائل والرد على الأزرار
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chosen_location = context.user_data.get("location", "ولاية حضرموت")
    
    if text in ["🕌 مواقيت الصلاة", "📆 التقويم الهجري", "📜 أحداث تاريخية"]:
        loc_info = LOCATIONS[chosen_location]
        data = get_islamic_data(loc_info['city'], loc_info['country'])
        
        if not data:
            await update.message.reply_text("عذراً، حدث خطأ أثناء جلب البيانات من الخادم.")
            return

        if text == "🕌 مواقيت الصلاة":
            timings = data['timings']
            msg = (
                f"🕌 مواقيت الصلاة في {chosen_location}:\n\n"
                f"🔹 الفجر: {timings['Fajr']}\n"
                f"🔹 الشروق: {timings['Sunrise']}\n"
                f"🔹 الظهر: {timings['Dhuhr']}\n"
                f"🔹 العصر: {timings['Asr']}\n"
                f"🔹 المغرب: {timings['Maghrib']}\n"
                f"🔹 العشاء: {timings['Isha']}\n"
            )
            await update.message.reply_text(msg)

        elif text == "📆 التقويم الهجري":
            hijri = data['date']['hijri']
            gregorian = data['date']['gregorian']
            msg = (
                f"📆 التاريخ الحالي:\n\n"
                f"🌙 الهجري: {hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ\n"
                f"📅 الميلادي: {gregorian['date']} م\n"
            )
            await update.message.reply_text(msg)

        elif text == "📜 أحداث تاريخية":
            hijri = data['date']['hijri']
            day = hijri['day']
            month_num = hijri['month']['number']
            date_key = f"{int(month_num):02d}-{int(day):02d}"
            event = ISLAMIC_EVENTS.get(date_key, "لا توجد أحداث رئيسية مسجلة في هذا اليوم التاريخي.")
            msg = f"📜 أحداث حصلت في مثل هذا اليوم ({day} {hijri['month']['ar']}):\n\n🔹 {event}"
            await update.message.reply_text(msg)

    elif text == "⚙️ ضبط الولاية":
        state_keyboard = [[state] for state in LOCATIONS.keys()]
        await update.message.reply_text(
            "الرجاء اختيار الولاية لتحديث المواقيت لها:",
            reply_markup=ReplyKeyboardMarkup(state_keyboard, resize_keyboard=True)
        )
        
    elif text in LOCATIONS:
        context.user_data["location"] = text
        await update.message.reply_text(f"✅ تم تغيير الموقع بنجاح إلى: {text}", reply_markup=get_main_keyboard())

# الدالة التشغيلية الرئيسية
def main():
    if not BOT_TOKEN:
        print("خطأ: لم يتم العثور على BOT_TOKEN في متغيرات البيئة!")
        return
        
    # قمنا بإلغاي تعارض الـ job_queue المسبب للمشكلة
    app = Application.builder().token(BOT_TOKEN).job_queue(None).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    
    print("البوت يقلع الآن بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
            
