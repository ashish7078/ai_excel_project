# 🧠 AI-Powered Excel Engine

## 📝 Overview

The AI-Powered Excel Engine is a backend application built with Python (FastAPI + Pandas) that enables users to interact with Excel files using natural language queries.

It can process queries like “show users where Purchase_Amount > 5000” or “find average purchase amount by city”, and returns clean, JSON-formatted responses.

This forms the foundation of an AI data assistant capable of analyzing and transforming Excel data intelligently.

## ⚙️ Features

-   📂 Upload and read Excel sheets dynamically
-   💬 Query Excel data using natural language
-   🧮 Perform operations like filtering, sorting, aggregation, and basic math
-   🔢 Create new columns with computed results (addition, subtraction, multiplication, division)
-   🧾 Handle timestamps and data serialization automatically
-   🧠 Designed for integration with local LLaMA models for offline NLP
-   🚀 Fast, lightweight, and extendable with minimal dependencies

## 🗂️ Project Structure
ai_excel_project/
│
├── fastapi_excel_api.py       # Main FastAPI application and endpoints
├── excel_engine.py            # Handles all Pandas-based Excel logic
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (e.g., Google API key)
├── .gitignore                 # Ignored files and folders
└── README.md                  # Project documentation

## 🧩 How to Run

### 🔧 Prerequisites

-   Python 3.9 or higher
-   `pip` installed
-   Virtual environment (recommended)
-   Postman or cURL for API testing

### 🚀 Steps

1.  **Clone the repository**
    ```sh
    git clone https://github.com/ashish7078/ai_excel_project.git
    cd ai_excel_project
    ```

2.  **Create and activate virtual environment**
    ```sh
    python -m venv venv
    ```
    *On Windows:*
    ```sh
    venv\Scripts\activate
    ```
    *On macOS/Linux:*
    ```sh
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Create `.env` file**
    Create a file named `.env` in the root directory and add your API key:
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```

5.  **Run the FastAPI server**
    ```sh
    uvicorn fastapi_excel_api:app --reload
    ```
    The server will run at: `http://127.0.0.1:8000`

## 🧪 Sample Usage (Postman Testing)

### ➤ 1. Upload Excel File

-   **Method:** `POST`
-   **URL:** `http://127.0.0.1:8000/upload`
-   **Body (form-data):**
    -   Key: `file`
    -   Type: `File`
    -   Value: (Select your Excel file) (Ex: 'data.xlsx')

**✅ Response:**
    ```json
    {
     "message": "File 'data.xlsx' uploaded successfully",
     "sheets": ["Sheet1", "Users", "Purchases"]
    }


### ➤ 2. Run a Query

-   **Method:** `POST`
-   **URL:** `http://127.0.0.1:8000/ai_query/data.xlsx/Sheet1`
-   **Body (raw JSON):**
    ```json
    {
      "query": "Show top 5 users with highest Purchase_Amount",
    }
    ```

**✅ Response:**
```json
[
  {
    "User_ID": "U1000",
    "Name": "User_0",
    "Purchase_Amount": 6429.7,
    "City": "Hyderabad"
  }
  {
    "User_ID": "U1020",
    "Name": "User_20",
    "Purchase_Amount": 7429.7,
    "City": "Mumbai"
  }
]