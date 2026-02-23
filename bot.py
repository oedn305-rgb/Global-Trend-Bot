import os
import smtplib
import sys
import google.generativeai as genai
from email.mime.text import MIMEText

# تثبيت المكتبة لضمان أحدث نسخة
os.system('pip install -q -U google-generativeai')

def run_global_trend_bot():
    try:
        api_key = os.getenv("GEMINI_KEY")
        sender_email = os.getenv("MY_EMAIL")
        app_password = os.getenv("EMAIL_PASS")
        target_email = "oedn305.Trand2@blogger.com" 

        genai.configure(api_key=api_key)

        # --- حل مشكلة الـ 404: البحث عن الموديل المتاح تلقائياً ---
        model_name = 'gemini-1.5-flash' # الافتراضي
        try:
            # محاولة التأكد من الموديلات المتاحة في حسابك
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    model_name = m.name
                    break
        except:
            model_name = 'models/gemini-1.5-flash' # العودة للاسم الكامل إذا فشل الحصر

        model = genai.GenerativeModel(model_name)

        # 1. طلب الترند العالمي
        trend_query = (
            "What is the top trending global topic today in Science, Tech, or Sports? "
            "Avoid Politics and Religion. Provide only the title in Arabic."
        )
        
        trend_result = model.generate_content(trend_query)
        chosen_topic = trend_result.text.strip()
        
        if not chosen_topic: return

        # 2. كتابة المقال
        article_prompt = (
            f"اكتب مقال HTML احترافي وشامل عن: {chosen_topic}. "
            "اجعل المقال طويلاً ومنسقاً بـ H1 و H2 ليناسب جوجل أدسنس، بدون حقوق ملكية."
        )
        
        article_response = model.generate_content(article_prompt)
        content = article_response.text.replace('```html', '').replace('```', '').strip()

        # 3. إرسال الإيميل
        msg = MIMEText(content, 'html', 'utf-8')
        msg['Subject'] = chosen_topic
        msg['From'] = sender_email
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح باستخدام موديل: {model_name}")

    except Exception as e:
        print(f"❌ خطأ تقني: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_global_trend_bot()
