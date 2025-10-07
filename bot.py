import logging
import os
from urllib.parse import quote_plus
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# التوكن الخاص بك
TOKEN = "7523578617:AAHECJgxEx-9FB9GN2lWoyJJHrunbzH-BwU" 

# تهيئة التسجيل
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# --- الدوال الخاصة بأوامر البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """الرد على أمر /start"""
    await update.message.reply_text(
        "مرحباً بك في بوت الكتب المجانية! 📚\n"
        "أرسل لي اسم الكتاب، وسأبحث لك عنه بصيغة PDF في المواقع المتاحة.",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """الرد على أمر /help"""
    await update.message.reply_text("طريقة الاستخدام بسيطة: أرسل اسم الكتاب للحصول على رابط بحث PDF جاهز.")

async def search_pdf_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إنشاء رابط بحث جوجل مُركز على ملفات PDF."""
    query = update.message.text # اسم الكتاب الذي أرسله المستخدم
    
    # 1. إنشاء رابط بحث مركز على موقع "مكتبة النور" وملف PDF
    # صيغة البحث في جوجل: 'site:al-maktaba.org "اسم الكتاب" filetype:pdf'
    alnoor_query = f'site:al-maktaba.org "{query}" filetype:pdf'
    encoded_alnoor = quote_plus(alnoor_query)
    alnoor_url = f"https://www.google.com/search?q={encoded_alnoor}"
    
    # 2. إنشاء رابط بحث عام عن الكتاب بصيغة PDF
    # صيغة البحث العامة: '"اسم الكتاب" filetype:pdf'
    general_query = f'"{query}" filetype:pdf'
    encoded_general = quote_plus(general_query)
    general_url = f"https://www.google.com/search?q={encoded_general}"

    response_text = (
        f"🔎 **نتائج البحث عن: '{query}'** 🔎\n\n"
        
        "1. **البحث المُركز في مكتبة النور** (الأكثر دقة):\n"
        f"[اضغط للبحث في مكتبة النور]({alnoor_url})\n\n"
        
        "2. **البحث العام عن PDF** (مصادر أخرى):\n"
        f"[اضغط للبحث في Google عن PDF]({general_url})\n\n"
        
        "**ملاحظة:** هذه الطريقة هي الأكثر استدامة وأماناً لحقوق النشر، حيث توجهك إلى نتائج البحث مباشرة.\n"
    )
            
    await update.message.reply_text(response_text, parse_mode='Markdown')


def main() -> None:
    """تشغيل البوت."""
    application = Application.builder().token(TOKEN).build()

    # إضافة Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_pdf_link))

    # **هام:** كما ناقشنا، يجب تغيير هذه الدالة إلى Webhook عند النشر الفعلي.
    logger.info("البدء في وضع Polling... (للاختبار المحلي)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
  
