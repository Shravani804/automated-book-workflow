import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#Reviewing the content using Gemini model
def review_text(text: str) -> str:
    prompt = f"As a language editor, revise the passage below to improve sentence flow, fix grammar issues, and enhance clarity for better readability:\n\n{text}"

    model = genai.GenerativeModel(model_name="gemini-1.5-flash") 

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error during AI content generation: {e}")
        return "ERROR: Review failed."

def main():
    input_path = Path("data/chapter1_spun.txt")
    output_path = Path("data/chapter1_reviewed.txt")

    if not input_path.exists():
        print("❌ chapter1_spun.txt not found.")
        return

    spun_text = input_path.read_text(encoding="utf-8")
    reviewed_text = review_text(spun_text)
    output_path.write_text(reviewed_text, encoding="utf-8")

    print("✅ Reviewed content saved to chapter1_reviewed.txt")

if __name__ == "__main__":
    main()
