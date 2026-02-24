import os
import time
import random
import smtplib
import re
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. إعداداتك الشخصية (ضع بياناتك هنا)
# ==========================================
API_KEY = "ضـع_مفـتاح_الـ_API_هنا"
MY_EMAIL = "your-email@gmail.com"
EMAIL_PASS = "xxxx xxxx xxxx xxxx"  # كلمة سر التطبيقات (16 حرف)
BLOGGER_EMAIL = "secret-address@blogger.com"

# إعداد المكتبة
genai.configure(api_key=API_KEY)

def run_blogger_bot():
    # استخدمنا 1.5-flash لتجنب خطأ 503 Illegal Metadata ولأنه أسرع
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    topics = [
        "أهمية الأمن السيبراني في 2026",
        "كيف يغير الذكاء الاصطناعي حياتنا اليومية",
        "مستقبل التقنية الخضراء والطاقة النظيفة"
    ]
    topic = random.choice(topics)

    print(f"🚀 البدء: توليد مقال عن {topic}")

    try:
        # 2. طلب المحتوى مع إعدادات تقليل الأخطاء
        response = model.generate_content(
            f"اكتب مقال HTML احترافي وباللغة العربية عن {topic}. استخدم H2 و H3 وتنسيق جذاب.",
            generation_config={"temperature": 0.7}
        )
        
        # تنظيف النص من علامات البرمجة
        article_body = response.text
        article_body = re.sub(r'```html|```', '', article_body).strip()
        print("✅ تم توليد النص بنجاح.")

        # 3. إعداد الإيميل
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_body, 'html', 'utf-8'))

        # 4. الإرسال (استخدام SSL ومنفذ 465 لتفادي التعليق)
        print("📧 جاري الإرسال إلى بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"🏁 مبروك! المقال نُشر بنجاح.")

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_blogger_bot()
