import requests
import smtplib
import random
import re
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. إعداداتك الشخصية (امسح النص العربي وحط بياناتك)
# ==========================================
API_KEY = "AIzaSy..." # ضع هنا مفتاحك الذي يبدأ بـ AIza
MY_EMAIL = "your-email@gmail.com" # إيميلك الجيميل
EMAIL_PASS = "xxxx xxxx xxxx xxxx" # كلمة سر التطبيقات (16 حرف)
BLOGGER_EMAIL = "secret-email@blogger.com" # إيميل بلوجر السري

# ==========================================
# 2. إعدادات الموديل (أحدث إصدار Gemini 2.0 Flash)
# ==========================================
MODEL_NAME = "gemini-2.0-flash"

def generate_and_send():
    # اختيار موضوع احترافي
    topics = [
        "أهمية الأمن السيبراني في عام 2026",
        "كيفية استخدام الذكاء الاصطناعي في تحسين الإنتاجية",
        "مستقبل الحوسبة السحابية وحماية البيانات"
    ]
    topic = random.choice(topics)
    
    print(f"🚀 البدء باستخدام أحدث موديل: {MODEL_NAME}")
    print(f"📝 جاري توليد مقال عن: {topic}")

    # الرابط المباشر للسيرفر
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"اكتب مقال HTML احترافي وطويل باللغة العربية عن {topic}. استخدم عناوين H2 و H3 وتنسيق جذاب للمدونات."
            }]
        }]
    }

    try:
        # طلب المحتوى
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ خطأ من جوجل ({response.status_code}): تأكد من أن الـ API KEY صحيح ومفعل.")
            return

        result = response.json()
        article_html = result['candidates'][0]['content']['parts'][0]['text']
        
        # تنظيف النص من علامات المارك داون
        article_html = re.sub(r'```html|```', '', article_html).strip()
        print("✅ تم توليد المقال بنجاح.")

        # إعداد الإيميل
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_html, 'html', 'utf-8'))

        # الإرسال عبر SMTP SSL (المنفذ 465 هو الأضمن)
        print("📧 جاري الإرسال إلى بلوجر...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"🏁 تم النشر بنجاح! اذهب لمدونتك وشاهد النتيجة.")

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    generate_and_send()
