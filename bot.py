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
        print(f"❌ خطأ أثناء توليد المحتوى: {e}")
        return None

def run_blogger_bot():
    # جلب البيانات من الـ Secrets
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ تأكد من إضافة الإيميلات وكلمة مرور التطبيقات في GitHub Secrets!")
        return

    # قائمة مواضيع احترافية لجلب الزيارات وقبول أدسنس
    topics = [
        "دليل شامل للربح من التسويق بالعمولة في 2026",
        "كيفية استخدام الذكاء الاصطناعي لتطوير عملك الخاص",
        "خطوات عملية لحماية هاتفك وبياناتك من التجسس"،
        "أفضل طرق استثمار العملات الرقمية للمبتدئين",
        "أسرار تحسين محركات البحث SEO لتصدر نتائج جوجل"
    ]
    topic = random.choice(topics)
    
    print(f"🚀 جاري توليد ونشر مقال عن: {topic}")

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
            print(f"✅ مبروك! المقال نُشر بنجاح الآن في مدونتك.")
        except Exception as e:
            print(f"❌ فشل إرسال الإيميل: {e}")
    else:
        print("❌ فشل توليد المقال، لن يتم الإرسال.")

if __name__ == "__main__":
    run_blogger_bot()
