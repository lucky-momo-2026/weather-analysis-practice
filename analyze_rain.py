import csv #Rraingall_dataで書いていたのをcsvで呼び出す
import sys


MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

def load_rainfall_data(csv_path): #データ読み込み関数
    rainfall_data = {} #データの入れ物

    with open(csv_path,newline='', encoding='utf-8') as f:  #cvsを読み込む　ファイルを開くwith open()
        reader = csv.reader(f) #CVSを１行ずつ読む
        rows = [row for row in reader if row]  #if row 空行を除外する
        
    if not rows:  #データがなければエラー表示させる
        raise ValueError("CSVが空です")

    #先頭行がヘッダーか判定する（２列目が数値ならデータ。数値じゃないならヘッダー）
    start_index =0                          #↓
    try:
        float(rows[0][1])
    except (ValueError, IndexError):
        start_index = 1                     #↑  ↓から↑までがヘッダー判定

    for row in rows[start_index:]:  #データを辞書に入れる
        if len(row) < 13:  #行のチェック　if ~ raise ValueError(...)
            raise ValueError("各行は１３行（都市名＋１２か月）必要です")

        city = row[0].strip()  #都市名
        rain_list = [float(v) for v in row[1:13]]  #数値変換　文字列　→　数値
        rainfall_data[city] = rain_list  #辞書に格納

    if not rainfall_data:  #最終判定
        raise ValueError("読み込めるデータがありません")

    return rainfall_data

def main():
    if len(sys.argv) < 2:
        print("使い方：Python analyze_rain.py <csvファイルパス>")
        return

    csv_path = sys.argv[1]  #sys[1] は data.csv

    try:
        rainfall_data = load_rainfall_data(csv_path)  #読み込み
    except Exception as e:
        print(f"csv読み込みエラー; {e}")
        return

    for city, rain_list in rainfall_data.items():  #都市ごとに計算
        max_rain = max(rain_list)
        min_rain = min(rain_list)
        avg_rain = sum(rain_list) / len(rain_list)

       #月ごとの特定
        max_months = [MONTHS[i] for i, v in enumerate(rain_list) if v == max_rain] #enumerat()は番号と値を扱うことができる
        min_months = [MONTHS[i] for i, v in enumerate(rain_list) if v == min_rain]

        print("----", city, "----")  #表示
        print("雨が最も多い月："," / ".join(max_months), f"{max_rain}mm")  #"/".joinで複数月を見やすく表示できる
        print("雨が最も少ない月："," / ".join(min_months), f"{min_rain}mm")
        print("年間平均降水量：", f"{avg_rain:.1f}mm")  #.1f　小数点１桁表示する

    ranking = sorted(            #ランキング　sorted(... key=...)で並び替えの基準を指定
        rainfall_data.items(),  
        key=lambda item: sum(item[1]) / len(item[1]),  #item[1]降水量リスト
        reverse=True  #大きい順で並べ替え
    ) 
      
    print("\n=== 年間平均降水量ランキング ===")  #\nとprint()は同じ意味　１行空ける
    for i, (city, rain_list) in enumerate(ranking, start=1):  #順位の表示　enumerate(..., start=1)で１位から始める
        avg_rain = sum(rain_list) / len(rain_list)
        print(f"{i}位： {city} ({avg_rain:.1f}mm)")

if __name__ == "__main__":
    main()