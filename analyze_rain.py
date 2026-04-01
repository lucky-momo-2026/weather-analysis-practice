import csv #Rraingall_dataで書いていたのをcsvで呼び出す
import sys


MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

def load_rainfall_data(csv_path):
    rainfall_data = {}

    with open(csv_path,newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]  #空行を除外する
        
    if not rows:
        raise ValueError("CSVが空です")

    #先頭行がヘッダーか判定する（２列目が数値でなければヘッダーとみなす
    start_index =0
    try:
        float(rows[0][1])
    except (ValueError, IndexError):
        stat_index = 1

    for row in rows[stat_index:]:
        if len(row) < 13:
            raise ValueError("各行は１３行（都市名＋１２か月）必要です")

        city = row[0].strip()
        rain_list = [float(v) for v in row[1:13]]
        rainfall_data[city] = rain_list

    if not rainfall_data:
        raise ValueError("読み込めるデータがありません")

    return rainfall_data

def main():
    if len(sys.argv) < 2:
        print("使い方：Python analyze_rain.py <csvファイルパス>")
        return

    csv_path = sys.argv[1]

    try:
        rainfall_data = load_rainfall_data(csv_path)
    except Exception as e:
        print(f"csv読み込みエラー; {e}")
        return

    for city, rain_list in rainfall_data.items():
        max_rain = max(rain_list)
        min_rain = min(rain_list)


        max_months = [MONTHS[i] for i, v in enumerate(rain_list) if v == max_rain] #enumerat()は番号と値を扱うことができる
        min_months = [MONTHS[i] for i, v in enumerate(rain_list) if v == min_rain]
        min_month_index = rain_list.index(min_rain)

        print("----", city, "----")
        print("雨が最も多い月："," / ".join(max_months), f"{max_rain}mm")  #"/".joinで複数月を見やすく表示できる
        print("雨が最も少ない月："," / ".join(min_months), f"{min_rain}mm")
        print()

if __name__ == "__main__":
    main()