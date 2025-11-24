# Software Requirements Specification (SRS)
## Project: Smart Receipt Scanner & Expense Analyzer

### 1. Introduction
This software extracts text from receipt images using OCR, auto-categorizes the expense, and displays basic analytics.

### 2. Functional Requirements
- FR1: User can upload receipt image.
- FR2: System extracts text from image.
- FR3: System detects total amount.
- FR4: System categorizes expense.
- FR5: System returns output to frontend.

### 3. Non-Functional Requirements
- NFR1: OCR should work within 5 seconds.
- NFR2: UI should be simple to use.
- NFR3: Should run on low-end machines.
- NFR4: Should not permanently store images.

### 4. Software Requirements
- Python 3.x
- Flask
- pytesseract
- Pillow

### 5. Hardware Requirements
- 4GB RAM
- Any OS with Python support
