import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_structured_data(rows=1000):
    np.random.seed(42)

    user_ids = [f"U{1000 + i}" for i in range(rows)]
    names = [f"User_{i}" for i in range(rows)]
    ages = np.random.randint(18, 60, size=rows)
    join_dates = pd.to_datetime(
        np.random.randint(
            int(datetime(2020, 1, 1).timestamp()),
            int(datetime(2025, 1, 1).timestamp()),
            size=rows
        ),
        unit='s'
    )
    last_active = [d + timedelta(days=np.random.randint(0, 365)) for d in join_dates]
    purchase_amount = np.round(np.random.normal(5000, 1500, rows), 2)
    discount_percent = np.round(np.random.uniform(5, 50, rows), 2)
    city = np.random.choice(
        ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata"],
        size=rows
    )
    payment_method = np.random.choice(
        ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"],
        size=rows
    )
    is_premium = np.random.choice(["Yes", "No"], size=rows, p=[0.3, 0.7])

    df = pd.DataFrame({
        "User_ID": user_ids,
        "Name": names,
        "Age": ages,
        "City": city,
        "Join_Date": join_dates,
        "Last_Active": last_active,
        "Purchase_Amount": purchase_amount,
        "Discount_%": discount_percent,
        "Payment_Method": payment_method,
        "Is_Premium": is_premium
    })

    return df


def create_unstructured_data(rows=1000):
    np.random.seed(42)

    reviews = [
        "Amazing quality! Exceeded my expectations.",
        "Pretty decent for the price.",
        "Delivery took longer than expected.",
        "Customer service was quick to resolve my issue.",
        "Not satisfied with the build quality.",
        "Absolutely loved it, will recommend!",
        "Got a defective piece initially but replacement was fine.",
        "Packaging was neat and product works perfectly.",
        "Feels premium, worth every rupee.",
        "Would not buy again, disappointing experience."
    ]

    sentiment = ["Positive", "Neutral", "Negative"]
    ratings = np.random.randint(1, 6, size=rows)

    df = pd.DataFrame({
        "Review_ID": [f"R{10000 + i}" for i in range(rows)],
        "User_ID": [f"U{1000 + np.random.randint(0, rows)}" for _ in range(rows)],
        "Review_Text": [np.random.choice(reviews) for _ in range(rows)],
        "Rating": ratings,
        "Sentiment": [np.random.choice(sentiment, p=[0.5, 0.3, 0.2]) for _ in range(rows)],
        "Review_Date": pd.to_datetime(
            np.random.randint(
                int(datetime(2021, 1, 1).timestamp()),
                int(datetime(2025, 1, 1).timestamp()),
                size=rows
            ),
            unit='s'
        )
    })

    return df


if __name__ == "__main__":
    structured_df = create_structured_data()
    unstructured_df = create_unstructured_data()

    file_name = "realistic_synthetic_data.xlsx"
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        structured_df.to_excel(writer, sheet_name="Users_And_Purchases", index=False)
        unstructured_df.to_excel(writer, sheet_name="User_Reviews", index=False)

    print(f"Data generation complete! File saved as: {file_name}")
