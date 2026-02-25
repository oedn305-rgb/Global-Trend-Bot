import os
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# محاولة الاستيراد مع معالجة الخطأ
try:
    from duckduckgo_search import DDGS
except ImportError:
    os.system('pip install duckduckgo_search typing_extensions')
    from duckduckgo_search import DDGS

def run_blogger_bot():
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    topics = [
        "أفضل طرق استثمار المال في 2026",
        "كيفية تعلم الذكاء الاصطناعي من الصفر",
        "أسرار النجاح في العمل عبر الإنترنت"
    ]
    topic = random.choice(topics)
    
    print(f"🔄 جاري تحضير المقال عن: {topic}")

    try:
        # استخدام DDGS لتوليد المحتوى
        with DDGS() as ddgs:
            prompt = f"اكتب مقال HTML احترافي وطويل بالعربية عن {topic}. استخدم h2 و h3. اجعله مفيداً جداً ومقبولاً في أدسنس."
            # تحديد الموديل لضمان الجودة
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            
            if response:
                msg = MIMEMultipart()
                msg['Subject'] = topic
                msg['From'] = MY_EMAIL
                msg['To'] = BLOGGER_EMAIL
                msg.attach(MIMEText(response, 'html', 'utf-8'))

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(MY_EMAIL, EMAIL_PASS)
                    server.send_message(msg)
                print(f"✅ تم النشر بنجاح: {topic}")
            else:
                print("❌ فشل في الحصول على استجابة من الذكاء الاصطناعي")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_blogger_bot()
