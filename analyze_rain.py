import pandas as pd  #pandasライブラリを使えるようにする　pdは省略名
import sys  #csvファイルを受取るので変わらない


MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

def main():
    if len(sys.argv) < 2:
        print("使い方：Python analyze_rain.py <csvファイルパス>")
        return

    try:
        csv_path = sys.argv[1] 

        df = pd.read_csv(csv_path)  #読み込むからread
        df = df.set_index(df.columns[0])  # df.columns は DataFrame列名　ここではcity の部分から呼び出す

        tokyo = df.loc["東京"]

        print('最大降水量：', tokyo.max())
        print('最小降水量：', tokyo.min())
        print('平均降水量：', tokyo.mean())

        month = tokyo.idxmax()  # CSVが英語（月名）の場合は日本語に変換するために使う
        jp_month = MONTHS[list(df.columns).index(month)]  # 今回rainfall.csv の中身が英語なので、MONTHS を使った変換が必要
 
        print('最大降水月：', jp_month)

    except Exception as e:
        print(f"csv読み込みエラー; {e}")
        return

if __name__ == "__main__":
    main()