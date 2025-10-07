import logging
import os
from urllib.parse import quote_plus
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ----------------------------------------------------
# 1. الإعدادات الأولية
# ----------------------------------------------------

# تهيئة التسجيل
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# 2. الدوال الخاصة بالبوت (Handlers)
# ----------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """الرد على أمر /start وتقديم الترحيب."""
    await update.message.reply_text(
        "أهلاً بك يا طالب العلم! 📚 أنا جاهز لمساعدتك.\n"
        "أرسل لي اسم الكتاب الذي تبحث عنه، وسأوفر لك رابط بحث PDF موجه.",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """الرد على أمر /help."""
    await update.message.reply_text("طريقة الاستخدام: ببساطة، أرسل اسم الكتاب لتحصل على رابط بحث PDF جاهز.", parse_mode='Markdown')

async def search_pdf_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إنشاء رابط بحث جوجل مُركز على ملفات PDF والمكتبات العامة."""
    query = update.message.text
    
    await update.message.reply_text(f"جاري تجهيز روابط البحث عن: '{query}'...")

    # 1. رابط البحث المركز على "مكتبة النور" وملف PDF
    # صيغة البحث: 'site:al-maktaba.org "اسم الكتاب" filetype:pdf'
    alnoor_query = f'site:al-maktaba.org "{query}" filetype:pdf'
    encoded_alnoor = quote_plus(alnoor_query)
    alnoor_url = f"https://www.google.com/search?q={encoded_alnoor}"
    
    # 2. رابط البحث العام عن الكتاب بصيغة PDF في أي مكان
    general_query = f'"{query}" filetype:pdf'
    encoded_general = quote_plus(general_query)
    general_url = f"https://www.google.com/search?q={encoded_general}"

    response_text = (
        f"🔎 **نتائج البحث الموجه عن: '{query}'** 🔎\n\n"
        
        "1. **البحث في مكتبة النور** (غالباً يكون الأفضل للكتب):\n"
        f"[🔗 اضغط للبحث في مكتبة النور]({alnoor_url})\n\n"
        
        "2. **البحث العام عن PDF** (مصادر ومكتبات أخرى):\n"
        f"[🔗 اضغط للبحث في Google عن PDF]({general_url})\n\n"
        
        "**نصيحة:** الروابط أعلاه توجهك مباشرة لنتائج البحث، اختر منها ما يناسبك.\n"
    )
            
    await update.message.reply_text(response_text, parse_mode='Markdown')

# ----------------------------------------------------
# 3. دالة التشغيل الرئيسية (Main Function)
# ----------------------------------------------------

def main() -> None:
    """تشغيل البوت باستخدام Webhooks (مناسب لـ Railway/Heroku)."""
    
    # 1. قراءة التوكن من متغير البيئة (ضروري للأمان والنشر)
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') 
    
    if not TOKEN:
        logger.error("خطأ: لم يتم تحميل التوكن. يجب تعيين متغير البيئة TELEGRAM_BOT_TOKEN.")
        return
        
    # 2. قراءة المنفذ (PORT) الذي يوفره الخادم (مثل Railway)
    PORT = int(os.environ.get('PORT', 8080)) # القيمة الافتراضية 8080

    # 3. بناء التطبيق
    application = Application.builder().token(TOKEN).build()

    # 4. إضافة Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_pdf_link))

    # 5. تشغيل Webhook
    logger.info(f"البدء في وضع Webhook على المنفذ: {PORT}")
    
    # يجب أن يكون المسار (url_path) سرياً، لذلك نستخدم التوكن نفسه
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN, 
    )

if __name__ == "__main__":
    main()
    
