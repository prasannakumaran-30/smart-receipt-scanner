from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os
import json
import re
from flask_cors import CORS

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# ---- Helper: Load saved OCR results ----
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# ---- Helper: Save new OCR result ----
def save_data(record):
    data = load_data()
    data.append(record)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---- OCR Endpoint ----
@app.route("/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = "temp.jpg"
    img.save(img_path)

    # Run OCR
    text = pytesseract.image_to_string(Image.open(img_path))
    os.remove(img_path)

    amount = extract_amount(text)
    category = categorize(text)

    # Save for analytics
    if amount != "Not found":
        try:
            amount_float = float(amount)
        except:
            amount_float = None
        save_data({
            "amount": amount_float,
            "category": category
        })

    return jsonify({
        "raw_text": text,
        "amount": amount,
        "category": category
    })

# ---- Extract amount ----
def extract_amount(text):
    matches = re.findall(r"\d+\.\d{2}", text)
    return matches[-1] if matches else "Not found"

# ---- Categorization ----
def categorize(text):
    t = text.lower()
    if "food" in t or "restaurant" in t or "grill" in t:
        return "Food"
    if "uber" in t or "bus" in t or "ola" in t:
        return "Travel"
    if "movie" in t:
        return "Entertainment"
    if "mart" in t or "grocery" in t:
        return "Groceries"
    return "Others"

# ---- Analytics Endpoint ----
@app.route("/analytics", methods=["GET"])
def analytics():
    data = load_data()
    category_totals = {}
    total_sum = 0
    count = 0

    for item in data:
        amt = item.get("amount")
        cat = item.get("category", "Others")
        if amt is None:
            continue
        total_sum += amt
        count += 1
        category_totals[cat] = category_totals.get(cat, 0) + amt

    return jsonify({
        "count": count,
        "total_sum": round(total_sum, 2),
        "by_category": category_totals
    })

if __name__ == "__main__":
    app.run(debug=True)
