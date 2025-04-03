from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
import math

app = FastAPI()  # ✅ 先定义 app

# 尝试读取 Excel 文件
try:
    df = pd.read_excel("客户.xlsx")
except Exception as e:
    raise RuntimeError(f"无法读取客户.xlsx 文件: {e}")

# ✅ 然后再注册路由
@app.get("/query")
def query_keyword(keyword: str = Query(...)):
    if "客户搜索词" not in df.columns:
        return JSONResponse(status_code=500, content={"error": "数据表缺少 '客户搜索词' 字段。"})

    matches = df[df["客户搜索词"].str.strip().str.lower() == keyword.strip().lower()]

    if matches.empty:
        return {"match": False, "message": "未找到匹配的关键词。"}

    def safe_sum(col):
        try:
            val = matches[col].sum()
            return round(val, 2) if not math.isnan(val) and not math.isinf(val) else 0
        except:
            return 0

    summary = {
        "展示量": int(safe_sum("展示量")),
        "点击量": int(safe_sum("点击量")),
        "花费": safe_sum("花费"),
        "每次点击成本(CPC)": int(safe_sum("每次点击成本(CPC)")),
        "7天总销售额": safe_sum("7天总销售额"),
    }

    rows = matches.fillna("").to_dict(orient="records")

    return {
        "match": True,
        "rows": rows,
        "summary": summary
    }
