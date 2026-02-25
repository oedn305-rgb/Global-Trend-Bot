import os
import requests
import smtplib
import random
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run_blogger_bot():
    # الأسرار من GitHub
    API_KEY = os.getenv("GEMINI_KEY")
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([API_KEY, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ تأكد من إعداد Secrets: GEMINI_KEY, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL")
        return

    # مواضيع "ترند" ويحبها أدسنس وتحقق زيارات عالية
    topics = [
        "أفضل استراتيجيات العمل الحر عبر الإنترنت في 2026",
        "دليل شامل حول تطبيقات الذكاء الاصطناعي في التعليم والعمل",
        "كيفية بناء ميزانية مالية ناجحة وتحقيق الاستقلال المادي",
        "أسرار تحسين محركات البحث SEO لتصدر نتائج البحث",
        "مستقبل السيارات الكهربائية: هل تغنينا عن الوقود تماماً؟"
    ]
    topic = random.choice(topics)
    
    # الروابط الجديدة لعام 2026 لضمان العمل
    # سنستخدم v1beta لأنها تدعم أحدث الموديلات مجاناً
    MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY.strip()}"
    
    # برومبت احترافي لضمان جودة أدسنس
    prompt_text = f"""
    اكتب مقالاً احترافياً وحصرياً باللغة العربية عن "{topic}".
    المتطلبات لضمان قبول أدسنس:
    1. الطول: أكثر من 900 كلمة.
    2. التنسيق: استخدم HTML مع <h2> للعناوين الرئيسية و <h3> للفرعية.
    3. القيمة: أضف نصائح عملية، خطوات مرتبة، وخاتمة تلخص الموضوع.
    4. الجودة: تجنب الحشو، واجعل الأسلوب بشرياً وممتعاً.
    5. التفاعل: ابدأ بمقدمة تجذب القارئ وتطرح تساؤلات.
    6. SEO: ركز على الكلمات المفتاحية المتعلقة بـ {topic}.
    أخرج المحتوى بصيغة HTML مباشرة بدون مقدمات.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.7, "topP": 0.95, "maxOutputTokens": 4096}
    }

    try:
        response = requests.post(MODEL_URL, json=payload, timeout=60)
        
        # إذا فشل البرو (Pro)، ننتقل للفلاش (Flash) تلقائياً
        if response.status_code != 200:
            print("🔄 جاري تجربة الموديل البديل...")
            MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY.strip()}"
            response = requests.post(MODEL_URL, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            article_html = result['candidates'][0]['content']['parts'][0]['text']
            article_html = re.sub(r'```html|```', '', article_html).strip()

            # إرسال المقال
            msg = MIMEMultipart()
            msg['Subject'] = topic
            msg['From'] = MY_EMAIL
            msg['To'] = BLOGGER_EMAIL
            msg.attach(MIMEText(article_html, 'html', 'utf-8'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            
            print(f"✅ مبروك! المقال الاحترافي نزل الآن: {topic}")
        else:
            print(f"❌ خطأ فني من جوجل: {response.status_code}")

    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    run_blogger_bot()
