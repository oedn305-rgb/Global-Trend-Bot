import os
import sys

try:
    import google.generativeai as genai
    print("✅ Library installed successfully")
except ImportError:
    print("❌ Library 'google-generativeai' not found!")
    sys.exit(1)

# جلب المفتاح
gemini_key = os.getenv("GEMINI_KEY")

if not gemini_key:
    print("❌ GEMINI_KEY is missing from GitHub Secrets!")
    sys.exit(1)

try:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # تجربة بسيطة جداً للتأكد من الاتصال
    response = model.generate_content("Hi")
    if response:
        print("✅ Connection to Gemini is Successful!")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Detailed Error: {str(e)}")
    sys.exit(1)
