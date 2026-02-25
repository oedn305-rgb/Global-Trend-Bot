import os
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from duckduckgo_search import DDGS

def generate_pro_article(topic):
    """توليد مقال احترافي طويل متوافق مع أدسنس"""
    prompt = f"""
    اكتب مقالاً مفصلاً واحترافياً باللغة العربية عن موضوع: ({topic}).
    المتطلبات لضمان القبول في Google AdSense:
    1. الطول: أكثر من 800 كلمة.
    2. التنسيق: استخدم HTML فقط (h2, h3, p, ul, li).
    3. الهيكل: مقدمة مشوقة، فقرات غنية بالمعلومات، خاتمة قوية.
    4. الجودة: محتوى حصري 100% وأسلوب بشري بعيد عن التكرار.
    5. SEO: ركز على الكلمات المفتاحية لزيادة الزيارات.
    ابدأ بالمحتوى مباشرة بصيغة HTML.
    """
    
    try:
        with DDGS() as ddgs:
            # استخدام موديل متطور لضمان الجودة
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            if response:
                return response
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def run_blogger_bot():
    # جلب البيانات من الـ Secrets
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("Missing Secrets: Check MY_EMAIL, EMAIL_PASS, and BLOGGER_EMAIL")
        return

    # قائمة مواضيع احترافية - تم تصحيح الفواصل هنا
    topics = [
        "دليل شامل للربح من التسويق بالعمولة في 2026",
        "كيفية استخدام الذكاء الاصطناعي لتطوير عملك الخاص",
        "خطوات عملية لحماية هاتفك وبياناتك من التجسس",
        "أفضل طرق استثمار العملات الرقمية للمبتدئين",
        "أسرار تحسين محركات البحث SEO لتصدر نتائج جوجل"
    ]
    topic = random.choice(topics)
    
    print(f"Starting to generate article about: {topic}")

    article_content = generate_pro_article(topic)

    if article_content:
        # إعداد الرسالة
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        
        # إضافة تنسيق CSS بسيط ليظهر المقال بشكل جذاب في بلوجر
        styled_content = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; line-height: 1.8; color: #333;">
            {article_content}
        </div>
        """
        msg.attach(MIMEText(styled_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"Success! The article '{topic}' has been published.")
        except Exception as e:
            print(f"Email error: {e}")
    else:
        print("Failed to generate article content.")

if __name__ == "__main__":
    run_blogger_bot()
