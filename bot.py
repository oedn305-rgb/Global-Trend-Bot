import os
import smtplib
import sys
import google.generativeai as genai
from email.mime.text import MIMEText

# تثبيت المكتبة لضمان العمل في بيئة GitHub
os.system('pip install -q -U google-generativeai')

def run_global_trend_bot():
    try:
        # استدعاء المفاتيح من Secrets
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        
        # إيميل المدونة الجديدة الذي أرسلته
        target_email = "oedn305.Trand2@blogger.com" 

        if not api_key or not sender_email or not app_password:
            print("❌ هناك نقص في إعدادات Secrets في GitHub!")
            return

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # --- الخطوة 1: البحث عن أقوى ترند عالمي آمن ---
        trend_query = (
            "What is the most popular global trending topic today in Technology, Science, Health, or Sports? "
            "STRICTLY AVOID: Politics, Religion, Wars, and Scandals. "
            "The topic must be safe for Google AdSense. "
            "Provide only the title of the topic in Arabic."
        )
        
        trend_result = model.generate_content(trend_query)
        chosen_topic = trend_result.text.strip()
        
        if not chosen_topic:
            print("❌ لم يتم العثور على موضوع مناسب حالياً.")
            return

        print(f"🌍 الترند المختار للمدونة الجديدة: {chosen_topic}")

        # --- الخطوة 2: كتابة المقال بتنسيق SEO احترافي ---
        article_prompt = (
            f"اكتب مقال HTML احترافي، طويل (أكثر من 600 كلمة) وشامل عن: {chosen_topic}. "
            "شروط المقال لضمان ملايين الزيارات وقبول أدسنس:\n"
            "1. محتوى حصري 100% ومفيد جداً للقارئ.\n"
            "2. استخدم تنسيق HTML: عنوان H1 كبير، وعناوين فرعية H2 و H3، وقوائم.\n"
            "3. لا تذكر أي أسماء مواقع أخرى أو روابط خارجية.\n"
            "4. اجعل الأسلوب مشوقاً لجذب الزوار من محركات البحث.\n"
            "5. ممنوع ذكر السياسة أو الدين أو أي محتوى مخالف."
        )
        
        article_response = model.generate_content(article_prompt)
        content = article_response.text.replace('```html', '').replace('```', '').strip()

        # --- الخطوة 3: الإرسال الفوري لمدونة بلوجر ---
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = chosen_topic
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح في المدونة الجديدة: {chosen_topic}")

    except Exception as e:
        print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_global_trend_bot()
