# ... (جزء التعريفات والمفاتيح السابق) ...

def run_final_success():
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    topic = "تطور الهواتف الذكية في 2026"
    print(f"🚀 جاري النشر النهائي لـ: {topic}")
    
    try:
        # التوليد
        response = model.generate_content(f"اكتب مقال SEO احترافي HTML عن {topic}")
        article_html = response.text
        
        # الإرسال (تأكد من وجود Secrets في GitHub)
        msg = MIMEMultipart()
        msg['Subject'] = f"📱 جديد التقنية: {topic}"
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_html, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
            
        print("✅ تم التوليد والنشر بنجاح باهر!")
    except Exception as e:
        print(f"❌ حدث خطأ بسيط في الخطوة الأخيرة: {e}")

if __name__ == "__main__":
    run_final_success()
