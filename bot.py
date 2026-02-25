import os
import smtplib
import random
import g4f
import re  # مكتبة التنظيف بالتعابير النمطية
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_pro_article(topic, internal_link):
    """توليد مقال صافي 100% بدون رغي زائد من الذكاء الاصطناعي"""
    # زدنا صرامة الأمر (Prompt) لمنع الثرثرة
    prompt = f"""
    اكتب مقالاً احترافياً طويلاً (1000 كلمة) بالعربية عن: ({topic}).
    التنسيق: HTML (h2, h3, p, table).
    مهم جداً: ابدأ مباشرة بـ <h2> ولا تكتب أي تحيات أو مقدمات مثل 'تفضل' أو 'إليك'.
    دمج الرابط الداخلي كفقرة 'اقرأ أيضاً': {internal_link}
    لا تضع علامات ```html في البداية أو النهاية.
    """
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )
        if response:
            # --- عملية التنظيف (The Filter) ---
            # 1. إزالة علامات الكود البرمجي إذا وجدت
            clean_text = re.sub(r'```html|```', '', response).strip()
            
            # 2. البحث عن أول وسم HTML والبدء منه (لحذف أي كلام قبله)
            start_index = clean_text.find('<h')
            if start_index != -1:
                clean_text = clean_text[start_index:]
            
            return clean_text
        return None
    except:
        return None

def run_blogger_bot():
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]): return

    my_pages = [
        "[https://trend-pulse24.blogspot.com/p/about-us.html?m=1](https://trend-pulse24.blogspot.com/p/about-us.html?m=1)",
        "[https://trend-pulse24.blogspot.com/p/privacy-policy.html?m=1](https://trend-pulse24.blogspot.com/p/privacy-policy.html?m=1)",
        "[https://trend-pulse24.blogspot.com/p/contact-us.html?m=1](https://trend-pulse24.blogspot.com/p/contact-us.html?m=1)",
        "[https://trend-pulse24.blogspot.com/p/disclaimer.html?m=1](https://trend-pulse24.blogspot.com/p/disclaimer.html?m=1)"
    ]
    selected_page = random.choice(my_pages)

    # قائمة مواضيع متنوعة (تقنية ورياضية) لضمان القبول
    topics = [
        "دليل الربح من التسويق بالعمولة 2026",
        "أهم انتقالات اللاعبين في الدوري السعودي 2026",
        "كيفية استخدام الذكاء الاصطناعي في الأعمال",
        "أسرار حماية البيانات من الاختراق",
        "تحليل مباريات دوري أبطال أوروبا القادمة"
    ]
    topic = random.choice(topics)

    article_content = generate_pro_article(topic, selected_page)

    if article_content:
        # محرك الصور المباشر (JPG) لضمان الظهور في بلوجر
        img_id = random.randint(10, 1000)
        image_url = f"[https://picsum.photos/id/](https://picsum.photos/id/){img_id}/800/450.jpg"
        
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        
        # تنسيق المقال النهائي (بدون أي كلام زائد)
        styled_content = f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: auto;">
            <div style="text-align:center; margin-bottom: 20px;">
                <img src="{image_url}" style="width:100%; max-width:600px; border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"/>
            </div>
            {article_content}
            <br/>
            <div style="background:#f9f9f9; padding:20px; border-right: 5px solid #1a73e8; border-radius:5px; margin-top:30px;">
                <strong>اقرأ المزيد في موقعنا:</strong><br/>
                <a href="{selected_page}" style="color:#1a73e8; text-decoration:none;">اضغط هنا لزيارة صفحتنا الرسمية ومعرفة المزيد</a>
            </div>
        </div>
        """
        
        msg.attach(MIMEText(styled_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"✅ تم النشر بنجاح (مقال نظيف): {topic}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_blogger_bot()
