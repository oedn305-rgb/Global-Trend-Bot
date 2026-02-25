import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from duckduckgo_search import DDGS # مكتبة مجانية تماماً بدون مفتاح

def generate_article(topic):
    prompt = f"اكتب مقالاً طويلاً واحترافياً باللغة العربية عن {topic}. استخدم تنسيق HTML بداخل المقال (h2, h3, p). اجعله متوافقاً مع سيو وأدسنس."
    
    try:
        with DDGS() as ddgs:
            # استخدام موديل GPT-4o-mini أو Llama 3 مجاناً
            results = ddgs.chat(prompt, model='gpt-4o-mini')
            return results
    except Exception as e:
        print(f"❌ خطأ في توليد المحتوى: {e}")
        return None

def run_blogger_bot():
    # الأسرار المطلوبة فقط للإيميل
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ نقص في إعدادات الإيميل بـ GitHub Secrets")
        return

    topics = [
        "أسرار النجاح في العمل الحر 2026",
        "كيفية حماية خصوصيتك على الإنترنت",
        "دليل شامل لتعلم البرمجة من الصفر"
    ]
    topic = random.choice(topics)
    print(f"📝 جاري توليد المقال عن: {topic} (بدون API Key)...")

    article_content = generate_article(topic)

    if article_content:
        # إرسال المقال لبلوجر
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"✅ تم النشر بنجاح! تفقد مدونتك الآن.")
        except Exception as e:
            print(f"❌ خطأ في إرسال الإيميل: {e}")
    else:
        print("❌ فشل توليد المقال.")

if __name__ == "__main__":
    run_blogger_bot()
