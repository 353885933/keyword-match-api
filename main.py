from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# 读取大型客户表格数据（内置加载）
try:
    df = pd.read_excel("客户.xlsx")
except Exception as e:
    raise RuntimeError(f"无法读取客户.xlsx 文件: {e}")

@app.get("/query")
def query_keyword(keyword: str = Query(...)):
    # 完全匹配关键词（忽略大小写与空格）
    matches = df[df["客户搜索词"].str.strip().str.lower() == keyword.strip().lower()]

    if matches.empty:
        return {"match": False, "message": "未找到匹配的关键词。"}

    summary = {
        "展示量": int(matches["展示量"].sum()),
        "点击量": int(matches["点击量"].sum()),
        "花费": round(matches["花费"].sum(), 2),
        "每次点击成本": int(matches["每次点击成本"].sum()),
        "7天总销售额": round(matches["7天总销售额"].sum(), 2),
    }

    return {
        "match": True,
        "rows": matches.to_dict(orient="records"),
        "summary": summary
    }
