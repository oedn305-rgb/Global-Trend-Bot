import os
import smtplib
import random
import g4f
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_pro_article(topic):
    """توليد مقال احترافي بلمسة بشرية وتنسيق سيو"""
    prompt = f"""
    اكتب مقالاً طويلاً جداً (أكثر من 1000 كلمة) باللغة العربية عن موضوع: ({topic}).
    يجب أن يتبع المقال هذا الترتيب:
    1. مقدمة جذابة تشرح أهمية الموضوع.
    2. جدول سريع يحتوي على أهم النقاط (استخدم وسم table).
    3. عدة عناوين فرعية (H2, H3) تشرح الموضوع بالتفصيل.
    4. قسم خاص بـ "نصائح الخبراء" لزيادة قيمة المحتوى.
    5. خاتمة قوية.
    استخدم تنسيق HTML احترافي، واجعل الأسلوب بشرياً وتثقيفياً تماماً.
    """
    
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )
        if response:
            return response
    except Exception as e:
        print(f"Generation Error: {e}")
        return None

def run_blogger_bot():
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("Missing Secrets!")
        return

    topics = [
        "دليل شامل للربح من التسويق بالعمولة في 2026",
        "كيفية استخدام الذكاء الاصطناعي لتطوير عملك الخاص",
        "خطوات عملية لحماية هاتفك وبياناتك من الاختراق",
        "أفضل طرق استثمار العملات الرقمية للمبتدئين",
        "أسرار تحسين محركات البحث SEO لتصدر نتائج جوجل",
        "مستقبل الوظائف في عصر الذكاء الاصطناعي",
        "كيف تبني مدونة ناجحة وتحقق منها أرباحاً مستمرة"
    ]
    topic = random.choice(topics)
    
    human_touches = [
        "أهلاً بكم زوارنا الكرام، اليوم سنتحدث عن موضوع يهم كل باحث عن النجاح وهو ",
        "في ظل الثورة الرقمية الحالية، قررنا في موقعنا تسليط الضوء على ",
        "هل تبحث عن الدليل الشامل لـ؟ اليوم سنكشف لك كل ما تحتاج معرفته عن "
    ]
    intro_touch = random.choice(human_touches)

    print(f"Starting to generate article about: {topic}")

    article_content = generate_pro_article(topic)

    if article_content:
        # نظام جلب صور احترافي ومباشر لضمان الظهور في بلوجر
        search_term = "technology" if "ذكاء" in topic or "هاتف" in topic else "business"
        img_id = random.randint(1, 1000)
        image_url = f"https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80&sig={img_id}"
        
        # وسم الصورة مع تنسيق يمنع الحظر من بلوجر
        image_tag = f'<div style="text-align:center; margin-bottom:20px;"><img src="{image_url}" alt="{topic}" style="width:100%; max-width:650px; border-radius:15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/></div>'
        
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        
        styled_content = f"""
        <div dir="rtl" style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #222; max-width: 800px; margin: auto; padding: 10px;">
            {image_tag}
            <p style="font-size: 1.2em; color: #444; border-right: 5px solid #1a73e8; padding-right: 15px;">{intro_touch} <strong>{topic}</strong>.</p>
            <br/>
            {article_content}
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-top: 30px; text-align: center;">
                <p><strong>هل أعجبك المقال؟</strong> لا تتردد في مشاركة رأيك في التعليقات!</p>
            </div>
        </div>
        """
        
        msg.attach(MIMEText(styled_content, 'html', 'utf-8'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(MY_EMAIL, EMAIL_PASS)
                server.send_message(msg)
            print(f"✅ Success! Published: {topic}")
        except Exception as e:
            print(f"Email error: {e}")
    else:
        print("❌ Failed to generate article.")

if __name__ == "__main__":
    run_blogger_bot()
