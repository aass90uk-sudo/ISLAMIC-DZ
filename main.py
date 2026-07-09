# main.py
import logging
import requests
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from config import BOT_TOKEN, LOCATIONS, ISLAMIC_EVENTS

# إعداد السجلات لتتبع الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# الأزرار المتواجدة داخل حقل الكتابة بنفس تصميم الصورة
def get_main_keyboard():
    keyboard = [
        ["🕌 مواقيت الصلاة", "📆 التقويم الهجري"],
        ["📜 أحداث تاريخية", "⚙️ ضبط الولاية"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, placeholder="اختر من القائمة أدناه...")

# دالة بدء البوت /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"أهلاً وسهلاً بك يا {user_name} في البوت الإسلامي الشامل.\n\n"
        "يسعدني تقديم خدمات التذكير بمواقيت الصلاة، التاريخ الهجري، والأحداث الإسلامية."
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())

# جلب مواقيت الصلاة والتاريخ الهجري من API خارجي موثوق
def get_islamic_data(city, country):
    try:
        url = f"https://aladhan.com{city}&country={country}&method=1"
        response = requests.get(url).json()
        if response['code'] == 200:
            return response['data']
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
    return None

# التعامل مع الأزرار والرد على المستخدم
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    # اختيار افتراضي للولاية إذا لم يختر المستخدم (يمكن تطويرها لحفظ خيار كل مستخدم)
    chosen_location = context.user_data.get("location", "ولاية حضرموت")
    loc_info = LOCATIONS[chosen_location]
    
    data = get_islamic_data(loc_info['city'], loc_info['country'])
    
    if not data:
        await update.message.reply_text("عذراً، حدث خطأ أثناء جلب البيانات. حاول مجدداً لاحقاً.")
        return

    if text == "🕌 مواقيت الصلاة":
        timings = data['timings']
        msg = (
            f"🕌 مواقيت الصلاة في {chosen_location} ليوم القيامة:\n\n"
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
        # عرض قائمة الولايات للاختيار بينها
        state_keyboard = [[state] for state in LOCATIONS.keys()]
        await update.message.reply_text(
            "الرجاء اختيار الولاية لتحديث المواقيت والتنبيهات لها:",
            reply_markup=ReplyKeyboardMarkup(state_keyboard, resize_keyboard=True)
        )
        
    elif text in LOCATIONS:
        context.user_data["location"] = text
        await update.message.reply_text(f"✅ تم تغيير الموقع بنجاح إلى: {text}", reply_markup=get_main_keyboard())

# دالة التذكير التلقائي اليومية (تُشغل عبر الـ Scheduler)
def daily_reminder_job(app: Application):
    # كود لإرسال رسائل تذكيرية يومية للمستخدمين المسجلين بقاعدة البيانات
    pass

def main():
    # بناء التطبيق
    app = Application.builder().token(BOT_TOKEN).build()

    # إضافة المتحكمات بالأوامر والرسائل
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    # تشغيل نظام التنبيهات المجدولة في الخلفية
    scheduler = BackgroundScheduler()
    # إعداد مهمة يومية الساعة 12 ليلاً لتحديث التذكيرات
    scheduler.add_job(lambda: daily_reminder_job(app), 'cron', hour=0, minute=0)
    scheduler.start()

    # بدء تشغيل البوت
    print("البوت يعمل الآن بنجاح...")
    app.run_polling()

if __name__ == '__main__':
    main()
      
