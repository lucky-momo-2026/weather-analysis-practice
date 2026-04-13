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
    jp_month = MONTH_MAP[month]
    print('最大降水月：', jp_month)

    min_month = rain.idxmin()  #降水最月の取得
    jp_min_month = MONTH_MAP[min_month]
    print('最小降水月：', jp_min_month)
    
    std = rain.std()  #標準偏差を出す
    threshold = avg + std * 1.5  #異常値の判定　平均を超えた月が異常 
    abnormal = rain[rain > threshold]  #しきい値を超えた月を取り出す

    if len(abnormal) == 0:
        print('異常値なし')
    else:
        for month, value in abnormal.items():  #異常がある月を１つずつ取り出す
            jp_month = MONTH_MAP[month]  #月番号を日本語に変換
            print(f'☔異常値あり：{jp_month} {value}mm')
    
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

    #グラフ表示都市名と都市を分ける
    city_names = ['札幌', '東京', '名古屋', '大阪', '福岡']
    years = ['2023', '2024']

    #年ごとの平均降水量を取り出す
    data_by_year = {}
    for year in years:
        data_by_year[year] = [avg_rain[f'{city}_{year}'] for city in city_names]

    plt.figure(figsize=(15,5))  #全体のサイズ
    
    #棒グラフグループ
    plt.subplot(1, 2, 1)
    x = range(len(city_names))  #都市の位置
    plt.bar([i - 0.2 for i in x], data_by_year['2023'], width=0.4, label='2023年')
    plt.bar([i + 0.2 for i in x], data_by_year['2024'], width=0.4, label='2024年') 
    plt.xticks(x, city_names)  #都市名を表示
    plt.title('平均降水量比較（棒グラフ）')
    plt.ylabel('降水量(mm)')
    max_value = max(max(data_by_year['2023']),max(data_by_year['2024']))
    plt.ylim(0, max_value * 1.1)
    plt.legend()  #凡例を表示
        
    #折れ線グラフ（２年分を重ねる）
    plt.subplot(1, 2, 2)
    plt.plot(city_names, data_by_year['2023'], marker='o', label="2023年")
    plt.plot(city_names, data_by_year['2024'], marker="o", label='2024年')
    plt.title('平均降水量比較（折れ線グラフ）')
    plt.ylabel('降水量(mm)')
    plt.legend()

    #合体グラフ（棒＋折れ線）
    plt.figure(figsize=(8,5))

    X = range(len(city_names))

    #棒グラフ(2023,2024)
    plt.bar([i - 0.2 for i in x], data_by_year['2023'], width=0.4, label='2023年(棒)')
    plt.bar([i + 0.2 for i in x], data_by_year['2024'], width=0.4, label='2024年(棒)')

    #折れ線グラフ(2023,2024)
    plt.plot(x, data_by_year['2023'], marker='o', label='2023年(線)')
    plt.plot(x, data_by_year['2024'], marker='o', label='2024年(線)')

    plt.xticks(x, city_names)
    plt.title('平均降水量比較(合体グラフ)')
    plt.ylabel('降水量(mm)')
    plt.legend()

    plt.tight_layout()
    plt.savefig('rainfall_combo.png')
    #plt.show()

def main():
    if len(sys.argv) < 2:
        print("使い方：Python analyze_rain.py <csvファイルパス>")
        return

    try:
        # 各都市ごとのデータを1行ずつ処理する
        csv_path = sys.argv[1]  #CVSのファイルのパスを取得
        
        #３番目以降の引数を都市名リストとして取得（なければ全都市）
        cities = sys.argv[2:] if len(sys.argv) >2 else []

        df = pd.read_csv(csv_path)  #読み込むからread
        df = df.set_index(df.columns[0])  # df.columns は DataFrame列名　ここではcity の部分から呼び出す
        month_total = df.sum()

        MONTH_MAP = {
            "1": "1月", "2": "2月", "3": "3月",
            "4": "4月", "5": "5月", "6": "6月",
            "7": "7月", "8": "8月", "9": "9月",
            "10": "10月", "11": "11月", "12": "12月"
        }
        
        avg_rain = {}  #都市名・平均降水量をセットで入れる辞書
        report_rows = []  #各都市の分析結果をCSVようにためるリスト

        #citiesに都市名が指定されている場合、該当行だけに絞り込む
        if cities:
            df = df[df.index.str.contains('|'.join(cities))]  #指定都市だけ残す


        for city, rain in df.iterrows():  # tokyo = df. loc[]は名前でその列のデータを抽出、for 〇, △ in df.iterrrows()は〇が行番号、△が行のデータ抽出
            report =print_city_report(city,rain, MONTH_MAP) #１年分の分析結果を受取る
            avg_rain[city] = report['平均降水量(mm)']  #集計用に平均だけ辞書へ入れる
            report_rows.append(report) #csvように１年分の結果をためる

        #print_summary(avg_rain)  #全年の集計結果を表示

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

        #都市名列を_で分割して、都市と年の２列に分ける
        report_df[['都市', '年']] = report_df['都市名'].str.split('_', expand=True)

        #問ごとに年順に並べ変えて、前年比を計算士や宇久する
        report_df = report_df.sort_values(by=['都市', '年']).reset_index(drop=True)
        
        #同じ都市の１つ前の行の平均降水量を取り出す（都市をまたがないようにgroupdyを使う）
        report_df['前年平均比(mm)'] = report_df.groupby('都市')['平均降水量(mm)'].shift(1)

        #前年との差(mm)を計算する
        report_df['前年比(mm)'] = report_df['平均降水量(mm)'] - report_df['前年平均比(mm)']

        #前年からの変化率(%)を計算する(小数点１桁)
        report_df['前年比(%)'] = ((report_df['前年比(mm)'] / report_df['前年平均比(mm)']) * 100).round(1)    

        #CSV出力する列を再集計っていする（前年比の列を追加）
        report_df = report_df[[
            '順位', '評価', '都市名',
            '最大降水量(mm)', '最小降水量(mm)', '平均降水量(mm)',
            '前年比(mm)', '前年比(%)',
            '最大降水月', '最小降水月'    
        ]]

        report_df.to_csv('rainfall_result.csv', index=False, encoding='utf-8-sig')  #CVS保存
        print('分析結果を rainfall_result.cvs に保存しました')

    except Exception as e:
        print(f"csv読み込みエラー; {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
