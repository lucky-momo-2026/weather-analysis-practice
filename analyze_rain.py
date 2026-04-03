import pandas as pd  #pandasライブラリを使えるようにする　pdは省略名
import sys  #csvファイルを受取るので変わらない


MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

def print_city_report(city, rain, MONTH_MAP):
    print(f' -----{city}----- ')
    print('最大降水量：', rain.max(), 'mm')
    print('最小降水量：', rain.min(), 'mm')

    avg = round(rain.mean(), 1)
    print('平均降水量：', avg, 'mm')

    month = rain.idxmax().capitalize()
    jp_month = MONTH_MAP[month]
    print('最大降水月：', jp_month)
    print()

    return avg


def main():
    if len(sys.argv) < 2:
        print("使い方：Python analyze_rain.py <csvファイルパス>")
        return

    try:
        # 各都市ごとのデータを1行ずつ処理する
        csv_path = sys.argv[1] 

        df = pd.read_csv(csv_path)  #読み込むからread
        df = df.set_index(df.columns[0])  # df.columns は DataFrame列名　ここではcity の部分から呼び出す
        month_total = df.sum()

        MONTH_MAP ={
            "Jan": "1月", "Feb": "2月", "Mar": "3月",
            "Apr": "4月", "May": "5月", "Jun": "6月",
            "Jul": "7月", "Aug": "8月", "Sep": "9月",
            "Oct": "10月", "Nov": "11月", "Dec": "12月"
        } 

        avg_rain = {}  #都市名・平均降水量をセットで入れる辞書

        for city, rain in df.iterrows():  # tokyo = df. loc[]は名前でその列のデータを抽出、for 〇, △ in df.iterrrows()は〇が行番号、△が行のデータ抽出
  
            avg = print_city_report(city,rain, MONTH_MAP)
            avg_rain[city] = avg

        print()
        print(' -----集計結果-----')
        top_city = max(avg_rain, key=avg_rain.get)
        print('平均降水量が最も多い都市：', top_city)
        print('平均降水量', avg_rain[top_city], 'mm')

    except Exception as e:
        print(f"csv読み込みエラー; {e}")
        return

if __name__ == "__main__":
    main()

    # python analyze_rain.py rainfall.csv