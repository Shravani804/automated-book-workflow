import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def spin_text(text: str) -> str:
    prompt = f"Rewrite the following content in a creative and engaging storytelling style:\n\n{text}"

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # or "gemini-1.5-pro"

    response = model.generate_content(prompt)

    return response.text.strip()

def main():
    input_path = Path("data/chapter1.txt")
    output_path = Path("data/chapter1_spun.txt")

    if not input_path.exists():
        print("❌ chapter1.txt not found.")
        return

    original_text = input_path.read_text(encoding="utf-8")
    spun_text = spin_text(original_text)
    output_path.write_text(spun_text, encoding="utf-8")

    print("✅ Spun content saved to chapter1_spun.txt")

if __name__ == "__main__":
    main()
