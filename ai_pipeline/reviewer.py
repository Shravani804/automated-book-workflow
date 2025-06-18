import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def review_text(text: str) -> str:
    prompt = f"Please review the following story and improve it for grammar, clarity, and flow:\n\n{text}"

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # You can switch to "gemini-1.5-pro"

    response = model.generate_content(prompt)

    return response.text.strip()

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
