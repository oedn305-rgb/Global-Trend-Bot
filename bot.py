def run_blogger_bot():
    # جلب الأسرار
    raw_api_key = os.getenv("GEMINI_KEY")
    MY_EMAIL = os.getenv("MY_EMAIL")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

    if not all([raw_api_key, MY_EMAIL, EMAIL_PASS, BLOGGER_EMAIL]):
        print("❌ خطأ: تأكد من ضبط GitHub Secrets بشكل صحيح.")
        return
    
    API_KEY = raw_api_key.strip()
    
    # تحديث الرابط للإصدار v1 لضمان الاستقرار
    MODEL_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    topic = random.choice([
        "أهم تقنيات الذكاء الاصطناعي في 2026",
        "مستقبل التدوين الآلي والربح من الإنترنت",
        "كيف تحمي بياناتك الرقمية من الاختراق"
    ])
    
    print(f"🚀 جاري توليد مقال احترافي عن: {topic}...")

    # تحسين البرومبت (Prompt) للحصول على نتائج HTML أنظف
    prompt_text = f"اكتب مقالاً طويلاً واحترافياً بصيغة HTML عن '{topic}'. استخدم وسوم <h2> و <h3> و <p> و <ul>. لا تضع وسم <html> أو <body>، فقط المحتوى."

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }

    try:
        response = requests.post(MODEL_URL, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ خطأ من API جوجل ({response.status_code}): {response.text}")
            return

        result = response.json()
        
        # التأكد من وجود محتوى في الرد
        if 'candidates' in result and result['candidates'][0].get('content'):
            article_html = result['candidates'][0]['content']['parts'][0]['text']
            # تنظيف الكود من علامات التنسيق الخاصة بـ Markdown
            article_html = re.sub(r'```html|```', '', article_html).strip()
        else:
            print("⚠️ لم يتم توليد محتوى، قد يكون السبب سياسات المحتوى (Safety Settings).")
            return

        # إرسال الإيميل
        msg = MIMEMultipart()
        msg['Subject'] = topic
        msg['From'] = MY_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg.attach(MIMEText(article_html, 'html', 'utf-8'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(MY_EMAIL, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"✅ تم النشر بنجاح! موضوع اليوم: {topic}")

    except Exception as e:
        print(f"❌ حدث خطأ فني: {e}")
