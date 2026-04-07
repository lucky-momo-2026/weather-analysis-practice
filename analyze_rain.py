import pandas as pd  #pandasライブラリを使えるようにする　pdは省略名
import matplotlib.pyplot as plt  #グラフを表示・保存するためのライブラリ
plt.rcParams['font.family'] = 'Yu Gothic'  #日本語フォントの設定
import sys  #csvファイルを受取るので変わらない


MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

#１都市分の行使量データを分析し、結果を表示して分析、結果を表示して分析結果を返す関数
def print_city_report(city, rain, MONTH_MAP):
    print(f' ------{city}------ ')
    print('最大降水量：', rain.max(), 'mm')
    print('最小降水量：', rain.min(), 'mm')

    avg = round(rain.mean(), 1)  #, 1 平均降水量を小数点１桁で計算
    print('平均降水量：', avg, 'mm')

    month = rain.idxmax()  # 最大の月を取得
    month = month.capitalize()  # 先頭を大文字にする
    jp_month = MONTH_MAP[month]
    print('最大降水月：', jp_month)

    min_month = rain.idxmin()  #降水最月の取得
    min_month = min_month.capitalize()  #先頭を大文字にする
    jp_min_month = MONTH_MAP[min_month]
    print('最小降水月：', jp_min_month)
    
    print()
      
    return{
        '都市名': city,
        '最大降水量(mm)': rain.max(),
        '最小降水量(mm)': rain.min(),
        '平均降水量(mm)': avg,
        '最大降水月': jp_month,
        '最小降水月': jp_min_month
    }

# 全都市の平均降水量データから、最も多い都市を表示する関数
def print_summary(avg_rain):
    print(' ------集計結果------ ')

    top_city = max(avg_rain, key=avg_rain.get)  # 平均降水量が一番大きい都市名を取得
    print('平均降水量最多都市：', top_city)
    print('平均降水量：', avg_rain[top_city], 'mm')

    low_city = min(avg_rain,key=avg_rain.get)  #平均降水量が一番少ない都市名を取得
    print('平均降水量最小都市：', low_city)
    print('平均降水量：', avg_rain[low_city], 'mm')

#平均降水量の棒グラフを表示(単体)
    cities = list(avg_rain.keys())  #都市名のリスト
    values = list(avg_rain.values())  #棒グラフのタイトル

    plt.figure(figsize=(15, 4))  #全体のサイズ

    plt.subplot(1, 3, 1)
    plt.bar(cities,values)  #棒グラフを作成
    plt.title('平均降水量(棒グラフ)')  #グラフのタイトル

    #折れ線グラフ（単体）
    plt.subplot(1, 3, 2)
    plt.plot(cities, values, marker='o')  #折れ線グラフ
    plt.title('平均降水量（折れ線グラフ）')

    #合体グラフ（棒＋折れ線）
    plt.subplot(1, 3, 3)
    plt.bar(cities,values, color='skyblue') #棒グラフ
    plt.plot(cities, values, marker='o', color='blue')  #折れ線グラフ
    plt.title('平均降水量（比較グラフ）')
    
    plt.tight_layout()  #レイアウト調整
    plt.savefig('all_graph.png')
    plt.show()

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

        MONTH_MAP ={  #fetch_rain.pyが読み込めるように英語読みを変える
            "1": "1月", "2": "2月", "3": "3月",
            "4": "4月", "5": "5月", "6": "6月",
            "7": "7月", "8": "8月", "9": "9月",
            "10": "10月", "11": "11月", "12": "12月"
        }
        avg_rain = {}  #都市名・平均降水量をセットで入れる辞書
        report_rows = []  #各都市の分析結果をCSVようにためるリスト


        for city, rain in df.iterrows():  # tokyo = df. loc[]は名前でその列のデータを抽出、for 〇, △ in df.iterrrows()は〇が行番号、△が行のデータ抽出
            report =print_city_report(city,rain, MONTH_MAP) #１年分の分析結果を受取る
            avg_rain[city] = report['平均降水量(mm)']  #集計用に平均だけ辞書へ入れる
            report_rows.append(report) #csvように１年分の結果をためる

        print_summary(avg_rain)  #全年の集計結果を表示

        report_df = pd.DataFrame(report_rows)   #リストを表に変換
        report_df = report_df.sort_values(by='平均降水量(mm)', ascending=False)  #平均降水量が多い順に並べ替え
        report_df['順位'] = range(1, len(report_df) + 1)  #順位を追加　１位からスタート

        def rank_label(rank):  #評価ランクを追加（S/A/B）
            if rank == 1:
                return 'S'
            elif rank <= 3:
                return 'A'
            else: return 'B'
        
        report_df['評価'] = report_df['順位'].apply(rank_label)

        report_df = report_df[['順位', '評価', '都市名','最大降水量(mm)', '最小降水量(mm)', '平均降水量(mm)', '最大降水月', '最小降水月']]
        report_df.to_csv('rainfall_result.csv', index=False, encoding='utf-8-sig')  #CVS保存
        print('分析結果を rainfall_result.cvs に保存しました')

    except Exception as e:
        print(f"csv読み込みエラー; {e}")
        return

if __name__ == "__main__":
    main()
