import os
import random
import time
import google.generativeai as genai

# 1. جلب المفاتيح من GitHub
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    print("❌ Error: GEMINI_KEY is missing!")
    exit(1)

# 2. إعداد الاتصال بالموديل المستقر
try:
    genai.configure(api_key=GEMINI_KEY)
    
    # استخدام موديل 2.0 فلاش لأنه الأحدث والأكثر توافقاً حالياً
    model = genai.GenerativeModel('gemini-2.0-flash')

    keywords = [
        "Future of Green Energy 2026", 
        "تطور الذكاء الاصطناعي في السعودية", 
        "NEOM projects 2026 updates",
        "أحدث تقنيات الهواتف الذكية"
    ]

    topic = random.choice(keywords)
    print(f"🚀 Processing: {topic}")

    # أمر الكتابة (Prompt)
    prompt = (
        f"Write a professional HTML article about {topic}.\n"
        "Structure: \n"
        "1. Arabic section inside <div dir='rtl'>\n"
        "2. English section inside <div dir='ltr'>\n"
        "Focus on 2026 news."
    )

    # 3. محاولة توليد المحتوى مع معالجة الزحام (Rate Limit)
    try:
        response = model.generate_content(prompt)
        
        if response.text:
            print("✅ Success! Article Generated.")
            print("-" * 20)
            print(response.text[:300]) # طباعة جزء للتأكد من السجلات
        else:
            print("⚠️ Warning: Received empty response.")
            
    except Exception as e:
        if "429" in str(e):
            print("❌ Error 429: Too many requests. Wait 10 minutes.")
        elif "404" in str(e):
            print("❌ Error 404: Model name issue. Check API version.")
        else:
            print(f"❌ Generation Error: {e}")
        exit(1)

except Exception as e:
    print(f"❌ Configuration Error: {e}")
    exit(1)
