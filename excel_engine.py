import pandas as pd
from datetime import datetime

class ExcelEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sheets = {}
        self.load_excel()

    # ----------------------------
    # Load Excel
    # ----------------------------
    def load_excel(self):
        try:
            xls = pd.ExcelFile(self.file_path)
            for sheet in xls.sheet_names:
                self.sheets[sheet] = xls.parse(sheet)
            print(f"✅ Loaded sheets: {list(self.sheets.keys())}")
        except Exception as e:
            print(f"⚠️ Failed to load Excel: {e}")

    # ----------------------------
    # Save Excel
    # ----------------------------
    def save_to_excel(self):
        """Save all modified sheets back to the same Excel file."""
        try:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='w') as writer:
                for sheet_name, df in self.sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"💾 Changes saved to {self.file_path}")
        except Exception as e:
            print(f"⚠️ Failed to save Excel: {e}")

    # ----------------------------
    # Update Sheet and Save
    # ----------------------------
    def update_sheet(self, sheet_name, df):
        """Replace sheet and save immediately."""
        try:
            self.sheets[sheet_name] = df
            self.save_to_excel()
        except Exception as e:
            print(f"⚠️ Error updating sheet '{sheet_name}': {e}")

    def get_sheet(self, sheet_name):
        return self.sheets.get(sheet_name, pd.DataFrame())

    # ----------------------------
    # Basic Math
    # ----------------------------
    def basic_math(self, sheet_name, col1, col2, operation, new_col_name):
        df = self.get_sheet(sheet_name)
        if df.empty:
            return df
        try:
            if operation == "add":
                df[new_col_name] = df[col1] + df[col2]
            elif operation == "subtract":
                df[new_col_name] = df[col1] - df[col2]
            elif operation == "multiply":
                df[new_col_name] = df[col1] * df[col2]
            elif operation == "divide":
                df[new_col_name] = df[col1] / df[col2]
            else:
                print("⚠️ Unsupported operation")

            self.update_sheet(sheet_name, df)
            return df
        except Exception as e:
            print(f"⚠️ Error in basic_math: {e}")
            return df

    # ----------------------------
    # Aggregations
    # ----------------------------
    def aggregations(self, sheet_name, group_by, target, agg_type, condition=None):
        df = self.get_sheet(sheet_name)
        if df.empty:
            return {"error": "Sheet not found or empty."}

        try:
            if condition:
                try:
                    df = df.query(condition)
                except Exception as e:
                    print(f"⚠️ Invalid filter condition: {e}")

            if not target:
                return {"error": "Missing 'target' field."}

            agg_type = agg_type.lower()

            if not group_by:
                result = pd.DataFrame()
                if agg_type == "sum":
                    result = pd.DataFrame([{f"{agg_type}_{target}": df[target].sum()}])
                elif agg_type in ["avg", "mean"]:
                    result = pd.DataFrame([{f"{agg_type}_{target}": df[target].mean()}])
                elif agg_type == "count":
                    result = pd.DataFrame([{f"{agg_type}_{target}": df[target].count()}])
                elif agg_type == "min":
                    result = pd.DataFrame([{f"{agg_type}_{target}": df[target].min()}])
                elif agg_type == "max":
                    result = pd.DataFrame([{f"{agg_type}_{target}": df[target].max()}])
                else:
                    return {"error": f"Invalid aggregation type: {agg_type}"}
                return result

            if agg_type == "sum":
                result = df.groupby(group_by)[target].sum().reset_index()
            elif agg_type in ["avg", "mean"]:
                result = df.groupby(group_by)[target].mean().reset_index()
            elif agg_type == "count":
                result = df.groupby(group_by)[target].count().reset_index()
            elif agg_type == "min":
                result = df.groupby(group_by)[target].min().reset_index()
            elif agg_type == "max":
                result = df.groupby(group_by)[target].max().reset_index()
            else:
                return {"error": f"Invalid aggregation type: {agg_type}"}

            result.columns = group_by + [f"{agg_type}_{target}"]
            for col in result.select_dtypes(include=["datetime64[ns]"]).columns:
                result[col] = result[col].astype(str)

            return result
        except Exception as e:
            print(f"⚠️ Error in aggregation: {e}")
            return {"error": str(e)}

    # ----------------------------
    # Filter
    # ----------------------------
    def filter_data(self, sheet_name, query_string, columns=None):
        data = self.get_sheet(sheet_name)
        if data.empty:
            return data
        try:
            temp_query = query_string
            for col in data.columns:
                if col in temp_query:
                    # This replace logic seems a bit redundant if using backticks, but keeping as-is
                    temp_query = temp_query.replace(col, f"{col}")
            
            filtered_data = data.query(temp_query)
            
            # This is the new part:
            if columns and isinstance(columns, list) and all(col in filtered_data.columns for col in columns):
                return filtered_data[columns]
            
            # If no columns are specified, return the whole filtered dataframe
            return filtered_data
        except Exception as e:
            print(f"Error in apply_filter: {e}")
            return pd.DataFrame()

    # ----------------------------
    # Sort
    # ----------------------------
    def sort_data(self, sheet_name, sort_by, ascending=True):
        df = self.get_sheet(sheet_name)
        if df.empty:
            return df
        try:
            sorted_df = df.sort_values(by=sort_by, ascending=ascending)
            self.update_sheet(sheet_name, sorted_df)
            return sorted_df
        except Exception as e:
            print(f"⚠️ Error in sort_data: {e}")
            return df

    # ----------------------------
    # Join
    # ----------------------------
    def join_sheets(self, left_sheet, right_sheet, on, how="inner", suffixes=("_left", "_right")):
        df_left = self.get_sheet(left_sheet)
        df_right = self.get_sheet(right_sheet)
        if df_left.empty or df_right.empty:
            return pd.DataFrame()
        try:
            joined_df = pd.merge(df_left, df_right, on=on, how=how, suffixes=suffixes)
            self.sheets["Joined_Result"] = joined_df
            self.save_to_excel()
            return joined_df
        except Exception as e:
            print(f"⚠️ Error in join_sheets: {e}")
            return pd.DataFrame()

    # ----------------------------
    # Pivot
    # ----------------------------
    def pivot_sheet(self, sheet_name, index, columns, values, aggfunc="sum"):
        df = self.get_sheet(sheet_name)
        if df.empty:
            return pd.DataFrame()
        try:
            pivot_df = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=0)
            pivot_df = pivot_df.reset_index()
            pivot_df.columns.name = None
            self.sheets[f"{sheet_name}_Pivot"] = pivot_df
            self.save_to_excel()
            return pivot_df
        except Exception as e:
            print(f"⚠️ Error in pivot_sheet: {e}")
            return pd.DataFrame()

    # ----------------------------
    # Unpivot
    # ----------------------------
    def unpivot_sheet(self, sheet_name, id_vars, value_vars, var_name="Variable", value_name="Value"):
        df = self.get_sheet(sheet_name)
        if df.empty:
            return pd.DataFrame()
        try:
            df.columns = [str(col) for col in df.columns]
            df = df.reset_index(drop=True)
            id_vars = [col for col in (id_vars if isinstance(id_vars, list) else [id_vars]) if col in df.columns]
            value_vars = [col for col in (value_vars if isinstance(value_vars, list) else [value_vars]) if col in df.columns]
            melted = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)
            self.sheets[f"{sheet_name}_Unpivoted"] = melted
            self.save_to_excel()
            return melted
        except Exception as e:
            print(f"⚠️ Error in unpivot_sheet: {e}")
            return pd.DataFrame()

    # ----------------------------
    # Top N
    # ----------------------------
    def top_n(self, sheet_name, sort_by, n=5, ascending=False):
        df = self.get_sheet(sheet_name)
        if df.empty:
            return pd.DataFrame()
        try:
            sorted_df = df.sort_values(by=sort_by, ascending=ascending).head(n)
            self.update_sheet(sheet_name, sorted_df)
            return sorted_df
        except Exception as e:
            print(f"⚠️ Error in top_n: {e}")
            return pd.DataFrame()

    # ----------------------------
    # Execute Query
    # ----------------------------
    def execute_query(self, sheet_name, query: dict):
        try:
            op = query.get("operation")
            if op == "filter":
                # This is the updated block
                return self.filter_data(
                    sheet_name, 
                    query.get("condition"), 
                    query.get("columns")  # Pass the new 'columns' list
                )

            elif op == "aggregations":
                return self.aggregations(sheet_name, query.get("group_by", []), query.get("target"),
                                         query.get("agg_type", "sum"), query.get("condition"))
            elif op == "sort":
                return self.sort_data(sheet_name, query.get("sort_by"), query.get("ascending", True))
            elif op == "top_n":
                return self.top_n(sheet_name, query.get("sort_by"), query.get("n", 5), query.get("ascending", False))
            elif op == "pivot":
                return self.pivot_sheet(sheet_name, query.get("index"), query.get("columns"),
                                        query.get("values"), query.get("aggfunc", "sum"))
            elif op == "unpivot":
                return self.unpivot_sheet(sheet_name, query.get("id_vars"), query.get("value_vars"),
                                          query.get("var_name", "Variable"), query.get("value_name", "Value"))
            elif op == "join":
                return self.join_sheets(query.get("left_sheet"), query.get("right_sheet"),
                                        query.get("on"), query.get("how", "inner"))
            elif op == "basic_math":
                return self.basic_math(sheet_name, query.get("col1"), query.get("col2"),
                                       query.get("operation_type"), query.get("new_col_name"))
            else:
                print(f"⚠️ Unknown operation: {op}")
                return pd.DataFrame()
        except Exception as e:
            print(f"⚠️ Error in execute_query: {e}")
            return pd.DataFrame()
