import os
import requests
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run_blogger_bot():
    # 1. جلب البيانات السرية
    API_KEY = os.getenv("GEMINI_KEY")
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([API_KEY, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ خطأ: تأكد من إضافة جميع الـ Secrets في GitHub (GEMINI_KEY, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL)")
        return

    # 2. تحديد المواضيع (مواضيع يحبها أدسنس: تعليمية، تقنية، نصائح)
    topics = [
        "دليل شامل لحماية البيانات الرقمية من الاختراق في 2026",
        "أفضل طرق الربح من الإنترنت للمبتدئين: استراتيجيات عملية",
        "كيفية استخدام الذكاء الاصطناعي في تحسين الإنتاجية اليومية",
        "أهم اتجاهات تكنولوجيا المعلومات التي ستغير العالم قريباً",
        "دليل المبتدئين لفهم العملات الرقمية وتقنية البلوكشين"
    ]
    topic = random.choice(topics)
    
    print(f"📝 جاري إعداد مقال حصري وعالي الجودة عن: {topic}")

    # 3. إعداد طلب Gemini مع "برومبت" احترافي لأدسنس
    MODEL_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY.strip()}"
    
    prompt = f"""
    اكتب مقالاً طويلاً ومفصلاً باللغة العربية عن '{topic}'.
    يجب أن يكون المقال متوافقاً مع معايير Google AdSense و SEO:
    1. استخدم تنسيق HTML (فقط محتوى المقال بدون وسوم html أو body).
    2. استخدم عناوين جذابة <h2> وعناوين فرعية <h3>.
    3. اكتب مقدمة مشوقة، فقرات مفصلة، وخاتمة قوية.
    4. أضف قائمة نقاط (bullet points) وجدولاً للمقارنة إذا كان ذلك مناسباً.
    5. اجعل الأسلوب احترافياً ومفيداً جداً للقارئ (محتوى ذو قيمة عالية).
    6. تجنب التكرار واجعل طول المقال لا يقل عن 800 كلمة.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(MODEL_URL, json=payload, timeout=40)
        if response.status_code != 200:
            print(f"❌ فشل في التواصل مع Gemini: {response.text}")
            return

        result = response.json()
        article_html = result['candidates'][0]['content']['parts'][0]['text']
        article_html = re.sub(r'```html|```', '', article_html).strip()

        # إضافة تنسيق CSS بسيط للمقال ليظهر بشكل رائع في بلوجر
        styled_html = f"""
        <div style="line-height: 1.8; font-size: 18px; color: #333; text-align: right; dir: rtl;">
            {article_html}
            <hr>
            <p style="font-style: italic; color: #777;">تم إعداد هذا المقال كدليل شامل لمساعدتكم في فهم {topic}.</p>
        </div>
        """

        # 4. إرسال المقال إلى بلوجر
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(styled_html, 'html', 'utf-8'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"✅ فخرنا بك! تم نشر المقال بنجاح الآن في مدونتك.")
        print(f"🔗 عنوان المقال: {topic}")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء التنفيذ: {e}")

if __name__ == "__main__":
    run_blogger_bot()
