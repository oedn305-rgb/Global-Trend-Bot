import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# استيراد المكتبة باسمها الجديد
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

def generate_pro_article(topic):
    """توليد مقال باستخدام الطريقة المحدثة للمكتبة"""
    prompt = f"اكتب مقالاً مفصلاً واحترافياً باللغة العربية عن موضوع: ({topic}). استخدم تنسيق HTML (h2, h3, p). اجعله متوافقاً مع أدسنس وسيو، وطويل أكثر من 800 كلمة."
    
    try:
        # الطريقة الجديدة للتعامل مع الموديل
        with DDGS() as ddgs:
            # استخدام chat بالشكل الجديد المستقر
            results = ddgs.chat(prompt, model='gpt-4o-mini')
            if results:
                return results
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
        "أسرار تحسين محركات البحث SEO لتصدر نتائج جوجل"
    ]
    topic = random.choice(topics)
    
    print(f"Starting to generate article about: {topic}")

    article_content = generate_pro_article(topic)

    if article_content:
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        
        styled_content = f"""
        <div dir="rtl" style="font-family: sans-serif; line-height: 1.8; color: #333;">
            {article_content}
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
