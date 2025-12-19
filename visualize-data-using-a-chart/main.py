import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

def main():
    # url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt"
    url = "ExcelFormattedGISTEMPDataCSV.csv"

    # 读取数据
    df = pd.read_csv(
        url,
        sep=',',
        skiprows=0,
        na_values=["***", "****"]  # 缺失值标记
    )

    df = df[["Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
    # 去掉缺失值
    df = df.dropna()
    # 按月批量处理并转换为摄氏度
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m in months:
        df[m] = df[m] / 100.0
    
    df["annual-mean"] = df[["Jan", "Feb", "Mar","Apr", "May", "Jun", "Jul", "Aug", "Sep","Oct", "Nov", "Dec"]].mean(axis=1)

    # 为 annual-mean 计算 Lowess 平滑（如果可用），否则使用 rolling 作为回退
    try:
        # frac 控制平滑程度：0.1 是一个合理的起点，可根据需要调整
        smoothed_vals = lowess(df["annual-mean"].values, df["Year"].values, frac=0.1, return_sorted=False)
        df["annual-mean-lowess"] = smoothed_vals
    except Exception:
        # 如果没有 statsmodels 可用，使用滚动平均作为替代（窗口大小可以调整）
        df["annual-mean-lowess"] = df["annual-mean"].rolling(window=11, center=True, min_periods=1).mean()

    plt.figure(figsize=(16, 8))

    # 原始年度平均（较细、半透明）
    plt.plot(df["Year"], df["annual-mean"], label="Annual Mean", color="blue", linewidth=1.2, alpha=0.8)
    # Lowess 平滑后的线（醒目颜色）
    plt.plot(df["Year"], df["annual-mean-lowess"], label="Lowess Smoothed", color="red", linewidth=2.0)
    plt.axhline(0, linestyle='--', color='gray', linewidth=0.8)  # 基线（1951–1980 平均）
    plt.xlabel("Year")
    plt.ylabel("Temperature Anomaly (°C)")
    plt.title("Global Temperature Anomaly (NASA GISTEMP) — Annual Mean with Lowess")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
