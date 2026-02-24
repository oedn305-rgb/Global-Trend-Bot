import os
import time
import random
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# 1. إعدادات المفاتيح (تأكد من ضبطها في بيئة العمل الخاصة بك)
GEMINI_KEY = os.getenv("GEMINI_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")  # كلمة سر التطبيقات (16 حرف)
BLOGGER_EMAIL = os.getenv("BLOGGER_EMAIL")

# إعداد جمناي
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') # تم التعديل للموديل المستقر المتاح حالياً

# 2. المواضيع (أضفت لك مواضيع تقنية لزيادة فرصة قبولك في أدسينس)
keywords = [
    "مستقبل الذكاء الاصطناعي في 2026", 
    "أمن المعلومات وحماية البيانات الشخصية", 
    "تطور تقنيات الحوسبة الكمية", 
    "أفضل أدوات الذكاء الاصطناعي للمبرمجين",
    "كيفية تحسين محركات البحث SEO للمواقع التقنية"
]
topic = random.choice(keywords)

# 3. توليد المقال
print(f"🚀 جاري كتابة مقال احترافي عن: {topic}")

# برومبت (Prompt) محسن ليعطيك نتائج SEO قوية
prompt = f"""
اكتب مقالاً احترافياً باللغة العربية حول موضوع: {topic}.
المتطلبات:
1. استخدم لغة HTML في التنسيق.
2. يجب أن يحتوي على عنوان رئيسي H1 وعناوين فرعية H2 و H3.
3. طول المقال لا يقل عن 600 كلمة.
4. اجعل الأسلوب بشرياً وتجنب التكرار الممل.
5. أضف فقرة عن 'رأينا التقني' لتعزيز قيمة المحتوى (E-E-A-T).
"""

try:
    response = model.generate_content(prompt)
    article_content = response.text

    # --- إضافة التحسينات (التنظيف) ---
    # إزالة أي علامات ```html أو علامات Markdown قد يضيفها الموديل
    article_content = re.sub(r'```html|```', '', article_content).strip()

    # 4. إعداد الإيميل
    msg = MIMEMultipart()
    msg['Subject'] = topic
    msg['From'] = MY_EMAIL
    msg['To'] = BLOGGER_EMAIL
    
    # ربط المحتوى كـ HTML لكي يظهر منسقاً في بلوجر
    msg.attach(MIMEText(article_content, 'html', 'utf-8'))

    # 5. عملية الإرسال الفعلي عبر SMTP
    print("📧 جاري الاتصال بسيرفر جوجل لإرسال المقال...")
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls() # تأمين الاتصال
        server.login(MY_EMAIL, EMAIL_PASS)
        server.send_message(msg)
    
    print(f"✅ تم النشر بنجاح! المقال الآن في طريقه لمدونتك: {topic}")

except Exception as e:
    print(f"❌ حدث خطأ تقني: {e}")
