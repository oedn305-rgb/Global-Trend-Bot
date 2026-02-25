import os
import smtplib
import random
import g4f
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_pro_article(topic, internal_link):
    """توليد مقال احترافي مع دمج رابط داخلي آلياً"""
    prompt = f"""
    اكتب مقالاً احترافياً طويلاً (1000 كلمة) بالعربية عن: ({topic}).
    التنسيق: HTML (h2, h3, p, table).
    مهم جداً: قم بدمج هذا الرابط الداخلي بشكل طبيعي داخل النص كفقرة "اقرأ أيضاً": {internal_link}
    اجعل الأسلوب بشرياً وتجنب التكرار لضمان قبول أدسنس.
    """
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )
        return response if response else None
    except:
        return None

def run_blogger_bot():
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]): return

    # قائمة الصفحات لعمل روابط داخلية آلية (Internal Links)
    my_pages = [
        "https://trend-pulse24.blogspot.com/p/about-us.html?m=1",
        "https://trend-pulse24.blogspot.com/p/privacy-policy.html?m=1",
        "https://trend-pulse24.blogspot.com/p/contact-us.html?m=1",
        "https://trend-pulse24.blogspot.com/p/disclaimer.html?m=1"
    ]
    selected_page = random.choice(my_pages)

    topics = [
        "دليل الربح من التسويق بالعمولة 2026",
        "كيفية استخدام الذكاء الاصطناعي في الأعمال",
        "أسرار حماية البيانات من الاختراق",
        "استثمار العملات الرقمية للمبتدئين",
        "تحسين محركات البحث SEO لتصدر النتائج"
    ]
    topic = random.choice(topics)

    article_content = generate_pro_article(topic, selected_page)

    if article_content:
        # محرك الصور الجديد: استخدام رابط مباشر بصيغة JPG لضمان القبول
        img_id = random.randint(10, 1000)
        image_url = f"https://picsum.photos/id/{img_id}/800/450.jpg"
        
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        
        # تصميم المقال مع الصورة والرابط الداخلي
        styled_content = f"""
        <div dir="rtl" style="font-family: Arial; line-height: 1.8; color: #333;">
            <div style="text-align:center;">
                <img src="{image_url}" style="width:100%; max-width:600px; border-radius:10px;"/>
            </div>
            <br/>
            {article_content}
            <br/>
            <div style="background:#f0f0f0; padding:15px; border-radius:5px; text-align:center;">
                <strong>اقرأ المزيد في موقعنا:</strong><br/>
                <a href="{selected_page}">اضغط هنا لزيارة صفحتنا الرسمية</a>
            </div>
        </div>
        """
        
        msg.attach(MIMEText(styled_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"✅ تم النشر بنجاح مع الرابط الداخلي: {topic}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_blogger_bot()
