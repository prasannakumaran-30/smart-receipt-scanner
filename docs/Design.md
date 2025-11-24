# Design Document

## 1. System Architecture
User (Frontend) → Flask API → OCR (Tesseract) → Categorizer → Response

## 2. Use Case
Actor: User
Use Cases:
- Upload Receipt
- Extract Text
- Detect Amount
- Categorize Expense

## 3. Sequence Diagram (Text)
User → Frontend: Upload image
Frontend → Backend: POST /ocr
Backend → OCR: Extract text
Backend → Category Module: Detect category
Backend → Frontend: JSON response

## 4. Data Flow
Image → OCR → Extracted Text → Amount Detection → Categorization → Output
