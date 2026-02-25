import os
import smtplib
import random
import g4f
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_pro_article(topic):
    """توليد مقال احترافي بلمسة بشرية وتنسيق سيو"""
    # أمر متطور لإجبار الذكاء الاصطناعي على كتابة محتوى ذو قيمة عالية
    prompt = f"""
    اكتب مقالاً طويلاً جداً (أكثر من 1000 كلمة) باللغة العربية عن موضوع: ({topic}).
    يجب أن يتبع المقال هذا الترتيب:
    1. مقدمة جذابة تشرح أهمية الموضوع.
    2. جدول سريع يحتوي على أهم النقاط (استخدم وسم table).
    3. عدة عناوين فرعية (H2, H3) تشرح الموضوع بالتفصيل.
    4. قسم خاص بـ "نصائح الخبراء" لتجنب مشكلة المحتوى الضعيف.
    5. خاتمة قوية مع دعوة للقراء للتعليق.
    استخدم تنسيق HTML احترافي، واجعل الأسلوب بشرياً وتثقيفياً تماماً وابتعد عن التكرار.
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

    # مواضيع متخصصة لجلب الزوار وقبول أدسنس
    topics = [
        "دليل شامل للربح من التسويق بالعمولة في 2026",
        "كيفية استخدام الذكاء الاصطناعي لتطوير عملك الخاص",
        "خطوات عملية لحماية هاتفك وبياناتك من الاختراق",
        "أفضل طرق استثمار العملات الرقمية للمبتدئين",
        "أسرار تحسين محركات البحث SEO لتصدر نتائج جوجل",
        "مستقبل الوظائف في عصر الذكاء الاصطناعي وكيف تستعد له",
        "كيف تبني مدونة ناجحة وتحقق منها آلاف الدولارات شهرياً"
    ]
    topic = random.choice(topics)
    
    # لمسات بشرية عشوائية للمقدمة (لخداع فلاتر الذكاء الاصطناعي)
    human_touches = [
        "أهلاً بكم زوارنا الكرام، اليوم سنتحدث عن موضوع يشغل بال الكثيرين وهو ",
        "في ظل التطور المتسارع الذي نشهده، قررنا اليوم في مدونتنا تسليط الضوء على ",
        "هل سألت نفسك يوماً كيف يمكنك البدء في؟ اليوم نقدم لك الدليل الكامل حول "
    ]
    intro_touch = random.choice(human_touches)

    print(f"Starting to generate article about: {topic}")

    article_content = generate_pro_article(topic)

    if article_content:
        # إضافة صورة احترافية من Unsplash تتغير حسب الموضوع
        image_tag = f'<img src="https://source.unsplash.com/800x450/?tech,{topic.split()[-1]}" alt="{topic}" style="width:100%; border-radius:15px; margin-bottom:20px;"/>'
        
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        
        # التنسيق النهائي للمقال (التصميم الذي سيراه الزائر)
        styled_content = f"""
        <div dir="rtl" style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #222; max-width: 800px; margin: auto;">
            {image_tag}
            <p style="font-size: 1.1em; font-style: italic; color: #555;">{intro_touch} <strong>{topic}</strong>.</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;"/>
            {article_content}
            <div style="background: #f1f3f4; padding: 20px; border-radius: 10px; margin-top: 30px;">
                <strong>💡 نصيحة الموقع:</strong> محتوى هذا المقال مقدم لأغراض تعليمية، تأكد دائماً من متابعة أحدث التطورات في هذا المجال.
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
