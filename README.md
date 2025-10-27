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
-   🚀 Fast, lightweight, and extendable with minimal dependencies
```
## 📁 Project Structure
ai_excel_project/
    |- fastapi_excel_api.py   # Main FastAPI application and endpoints
    |- excel_engine.py        # Handles all Pandas-based Excel logic
    |- requirements.txt       # Python dependencies
    |- .env                   # Environment variables (e.g., Google API key)
    |- .gitignore             # Ignored files and folders
    |- README.md              # Project documentation
```

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
    -   Value: (Select your Excel file) (Ex: 'realistic_synthetic_data.xlsx')

**✅ Response:**
```json
    {
     "message": "File 'realistic_synthetic_data.xlsx' uploaded successfully",
     "sheets": ["Users_And_Purchases", "User_Reviews"]
    }
```

### ➤ 2. Run a Query

-   **Method:** `POST`
-   **URL:** `http://127.0.0.1:8000/ai_query/realistic_synthetic_data.xlsx/Users_And_Purchases`
-   **Body (raw JSON):**
    ```json
    {
      "query": "Show top 5 users with highest Purchase_Amount"
    }
    ```

**✅ Response:**
```json
[
  {
    "User_ID": "U1125",
    "Name": "User_125",
    "Age": 32,
    "City": "Mumbai",
    "Join_Date": "2023-08-23T13:50:24",
    "Last_Active": "2024-05-08T13:50:24",
    "Purchase_Amount": 9706.62,
    "Discount_%": 37.22,
    "Payment_Method": "Cash on Delivery",
    "Is_Premium": "No"
  },
  {
    "User_ID": "U1473",
    "Name": "User_473",
    "Age": 46,
    "City": "Mumbai",
    "Join_Date": "2022-07-04T19:37:18",
    "Last_Active": "2023-01-17T19:37:18",
    "Purchase_Amount": 9664.88,
    "Discount_%": 49.64,
    "Payment_Method": "Net Banking",
    "Is_Premium": "No"
  },
  {
    "User_ID": "U1689",
    "Name": "User_689",
    "Age": 21,
    "City": "Kolkata",
    "Join_Date": "2023-03-13T20:46:52",
    "Last_Active": "2023-11-14T20:46:52",
    "Purchase_Amount": 9477.89,
    "Discount_%": 31.18,
    "Payment_Method": "Net Banking",
    "Is_Premium": "Yes"
  },
  {
    "User_ID": "U1674",
    "Name": "User_674",
    "Age": 22,
    "City": "Hyderabad",
    "Join_Date": "2022-03-14T20:31:03",
    "Last_Active": "2022-07-28T20:31:03",
    "Purchase_Amount": 9423.64,
    "Discount_%": 10.18,
    "Payment_Method": "UPI",
    "Is_Premium": "No"
  },
  {
    "User_ID": "U1203",
    "Name": "User_203",
    "Age": 51,
    "City": "Chennai",
    "Join_Date": "2022-01-16T08:19:09",
    "Last_Active": "2022-09-04T08:19:09",
    "Purchase_Amount": 9139.49,
    "Discount_%": 49.13,
    "Payment_Method": "UPI",
    "Is_Premium": "No"
  }
]