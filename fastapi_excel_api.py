from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import json
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from excel_engine import ExcelEngine
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI(title="AI-Powered Excel Engine")

# Directory for uploads
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store active engines (file_name -> ExcelEngine instance)
engines = {}

# Configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # 🔑 Add your valid key here


# -------------------------------
# 📂 1. Upload Excel File
# -------------------------------
@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith((".xlsx", ".xls")):
            raise HTTPException(status_code=400, detail="Only Excel files are allowed.")

        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        engine = ExcelEngine(file_location)

        # ✅ Clean numeric-like columns (%, commas, currency, etc.)
        for sheet_name, df in engine.sheets.items():
            for col in df.columns:
                if df[col].dtype == 'object':
                    s = df[col].astype(str)
                    if s.str.contains('%').any():
                        s = s.str.replace('%', '', regex=False)
                    s = s.str.replace(',', '', regex=False)
                    s = s.str.replace('₹', '', regex=False)
                    s = s.str.replace('Rs.', '', regex=False)
                    df[col] = pd.to_numeric(s, errors='ignore')

        engines[file.filename] = engine

        return {
            "message": f"File '{file.filename}' uploaded successfully",
            "sheets": list(engine.sheets.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# -------------------------------
# 📑 2. List Sheets
# -------------------------------
@app.get("/sheets/{file_name}")
async def list_sheets(file_name: str):
    engine = engines.get(file_name)
    if not engine:
        raise HTTPException(status_code=404, detail="File not found or not uploaded.")
    return {"sheets": list(engine.sheets.keys())}



# -------------------------------
# ⚙️ 3. Structured Query Execution
# -------------------------------
@app.post("/query/{file_name}/{sheet_name}")
async def query_sheet(file_name: str, sheet_name: str, body: dict):
    engine = engines.get(file_name)
    if not engine:
        raise HTTPException(status_code=404, detail="File not found or not uploaded.")

    try:
        result_df = engine.execute_query(sheet_name, body)

        # ✅ Auto-save updates (only if DataFrame changed)
        if isinstance(result_df, pd.DataFrame) and not result_df.empty:
            engine.sheets[sheet_name] = result_df
            with pd.ExcelWriter(engine.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                result_df.to_excel(writer, sheet_name=sheet_name, index=False)

        result_df = result_df.applymap(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)
        return JSONResponse(result_df.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# -------------------------------
# 🤖 4. AI Query Execution (Gemini)
# -------------------------------
@app.post("/ai_query/{file_name}/{sheet_name}")
async def ai_query(file_name: str, sheet_name: str, body: dict):
    engine = engines.get(file_name)
    if not engine:
        raise HTTPException(status_code=404, detail="File not found or not uploaded.")

    df = engine.get_sheet(sheet_name)
    if df.empty:
        raise HTTPException(status_code=404, detail="Sheet not found or empty.")

    user_query = body.get("query")
    if not user_query:
        raise HTTPException(status_code=400, detail="Missing 'query' field in request body.")

    columns = list(df.columns)

    # 🧠 Prompt for Gemini
    prompt = f"""
    You are a data reasoning assistant that converts natural language queries about Excel data
    into JSON commands for a Pandas-based Excel Engine.

    Available columns: {columns}

    Output only valid JSON. No markdown, no text.

    Schema examples:

    1️⃣ Filter:
    {{
      "operation": "filter",
      "condition": "Purchase_Amount > 5000"
    }}
    
    1️⃣
    Example for filtering (specific columns):
    {{
        "operation": "filter",
        "condition": "Department == 'Sales'",
        "columns": ["FirstName", "LastName"]
    }}


    2️⃣ Aggregation:
    {{
      "operation": "aggregations",
      "group_by": ["City"],
      "target": "Purchase_Amount",
      "agg_type": "sum",
      "condition": "`Purchase_Amount` < 5000"
    }}

    3️⃣ Sort:
    {{
      "operation": "sort",
      "sort_by": "Purchase_Amount",
      "ascending": false
    }}

    4️⃣ Top N:
    {{
      "operation": "top_n",
      "sort_by": "Purchase_Amount",
      "n": 10,
      "ascending": false
    }}

    5️⃣ Pivot:
    {{
      "operation": "pivot",
      "index": "City",
      "columns": "Product",
      "values": "Purchase_Amount",
      "aggfunc": "sum"
    }}

    6️⃣ Unpivot:
    {{
      "operation": "unpivot",
      "id_vars": ["City"],
      "value_vars": ["Jan_Sales", "Feb_Sales", "Mar_Sales"],
      "var_name": "Month",
      "value_name": "Sales"
    }}

    7️⃣ Join:
    {{
      "operation": "join",
      "left_sheet": "Users",
      "right_sheet": "Purchases",
      "on": "User_ID",
      "how": "inner"
    }}

    8️⃣ Basic Math:
    {{
      "operation": "basic_math",
      "col1": "Price",
      "col2": "Quantity",
      "operation_type": "multiply",
      "new_col_name": "Total_Value"
    }}

    9️⃣ Date Operation:
    {{
      "operation": "date_operation",
      "column": "Order_Date",
      "extract": "month"
    }}

    User query: "{user_query}"
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        # 🧹 Clean up code fences
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`")
            if "json" in raw_output:
                raw_output = raw_output.split("json", 1)[1]
            raw_output = raw_output.strip()
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3].strip()

        structured_query = json.loads(raw_output)

        # 🪵 Log Gemini response
        os.makedirs("logs", exist_ok=True)
        with open("logs/ai_response_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(
                f"\n---\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"📂 File: {file_name}, 🧾 Sheet: {sheet_name}\n"
                f"🗣️ User Query: {user_query}\n"
                f"🤖 Model Output:\n{response.text}\n"
                f"✅ Parsed JSON:\n{json.dumps(structured_query, indent=2)}\n"
            )

        # ✅ Execute query
        result_df = engine.execute_query(sheet_name, structured_query)

        # ✅ Just return the DataFrame (no saving)
        if isinstance(result_df, pd.DataFrame) and not result_df.empty:
            result_df = result_df.applymap(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)
            return JSONResponse(result_df.to_dict(orient="records"))
        else:
            return JSONResponse(result_df)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Model returned invalid JSON: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# -------------------------------
# 🧹 5. Health Check
# -------------------------------
@app.get("/")
def root():
    return {"message": "AI Excel Engine is running 🚀"}
