import os
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# 1. إعدادات المفاتيح
GEMINI_KEY = os.getenv("GEMINI_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. المواضيع
keywords = ["Future of AI 2026", "Green Energy Trends", "ترند التكنولوجيا", "تطور الهواتف الذكية"]
topic = random.choice(keywords)

# 3. توليد المقال
print(f"🚀 جاري كتابة مقال عن: {topic}")
prompt = f"Write a professional HTML article about {topic} in Arabic. Min 500 words with H2 tags."

try:
    response = model.generate_content(prompt)
    article_content = response.text

    # 4. أمر الإرسال الفعلي (هذا اللي كان ناقصك)
    msg = MIMEMultipart()
    msg['Subject'] = topic
    msg['From'] = MY_EMAIL
    msg['To'] = BLOGGER_EMAIL
    msg.attach(MIMEText(article_content, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(MY_EMAIL, EMAIL_PASS)
        server.send_message(msg)
    
    print("✅ تم الإرسال بنجاح إلى بلوجر!")

except Exception as e:
    print(f"❌ حدث خطأ: {e}")
