from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = "temp.jpg"
    img.save(img_path)

    text = pytesseract.image_to_string(Image.open(img_path))
    os.remove(img_path)

    amount = extract_amount(text)
    category = categorize(text)

    return jsonify({
        "raw_text": text,
        "amount": amount,
        "category": category
    })

def extract_amount(text):
    import re
    numbers = re.findall(r"\d+\.\d{2}", text)
    return numbers[-1] if numbers else "Not found"

def categorize(text):
    text_lower = text.lower()
    if "food" in text_lower or "restaurant" in text_lower:
        return "Food"
    if "uber" in text_lower or "bus" in text_lower:
        return "Travel"
    if "movie" in text_lower:
        return "Entertainment"
    return "Others"

if __name__ == "__main__":
    app.run(debug=True)
