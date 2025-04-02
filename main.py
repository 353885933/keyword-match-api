from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# 示例数据
data = {
    "客户搜索词": [
        "no drill shades", "no drill zebra blinds for windows", "no drill zebra blinds",
        "no drill zebra shades", "zebra blinds for windows no drill", "zebra blinds",
        "zebra blinds no drill", "no drill blinds", "zebra blinds for windows",
        "zebra blinds for windows cordless", "cordless zebra shades"
    ],
    "展示量": [179089, 64801, 57869, 56674, 55443, 51349, 44616, 34833, 32797, 32674, 29372],
    "点击量": [1114, 527, 470, 388, 492, 395, 321, 447, 189, 189, 193],
    "点击率(CTR)": ["0.6220%", "0.8133%", "0.8122%", "0.6846%", "0.8874%", "0.7692%", "0.7195%", "1.2833%", "0.5763%", "0.5784%", "0.6571%"],
    "每次点击成本(CPC)": ["$1.30", "$1.73", "$1.71", "$1.74", "$1.69", "$1.98", "$1.80", "$0.98", "$1.60", "$1.64", "$1.67"],
    "花费": ["$1,451.22", "$914.30", "$804.40", "$676.87", "$833.35", "$781.64", "$577.69", "$436.50", "$302.31", "$309.58", "$322.65"],
    "7天总销售额": ["$2,608.43", "$3,014.62", "$3,046.13", "$1,670.10", "$3,330.36", "$0.00", "$1,322.63", "$1,191.88", "$1,018.95", "$317.27", "$860.05"]
}
df = pd.DataFrame(data)

# 清洗货币和百分比列
def clean_column(col):
    return col.replace("[$,%]", "", regex=True).astype(float)

df["花费"] = clean_column(df["花费"])
df["7天总销售额"] = clean_column(df["7天总销售额"])

@app.get("/query")
def query_keyword(keyword: str = Query(..., description="完整客户搜索词")):
    filtered = df[df["客户搜索词"].str.lower() == keyword.strip().lower()]
    if filtered.empty:
        return {"match": False, "message": "未找到匹配的关键词"}

    total = {
        "展示量": int(filtered["展示量"].sum()),
        "点击量": int(filtered["点击量"].sum()),
        "花费": round(filtered["花费"].sum(), 2),
        "7天总销售额": round(filtered["7天总销售额"].sum(), 2),
    }

    result_rows = filtered.to_dict(orient="records")

    return {
        "match": True,
        "result": result_rows,
        "summary": total
    }
