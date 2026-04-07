import requests  #URLにアクセスしてHTMLを取得するライブラリ
from bs4 import BeautifulSoup  #HTMLから必要なデータを取り出すライブラリ
import time  #サーバーへの連続アクセスを防ぐために使う
import pandas as pd  #データをCSVに保存するため

#５大ドーム所在都市の気象コード
CITIES = {
    '札幌':{'prec_no': 14, 'block_no': 47412},
    '東京':{'prec_no': 44, 'block_no': 47662},
    '名古屋':{'prec_no':51, 'block_no': 47636},
    '大阪':{'prec_no': 62, 'block_no': 47772},
    '福岡':{'prec_no': 82, 'block_no': 47807},
}

# 気象庁のURLテンプレート
BASE_URL = "https://www.data.jma.go.jp/obd/stats/etrn/view/monthly_s1.php"

YEAR = 2023

def fetch_rain(city, prec_no, block_no, year):
    url = f"{BASE_URL}?prec_no={prec_no}&block_no={block_no}&year={year}"  #気象庁のURLを組み立てる
    
    response = requests.get(url)  #URLにアクセスしてHTMLを取得する
    response.encoding = 'utf-8'   
    soup = BeautifulSoup(response.text, 'html.parser')  #HTMLを解析する

    tables = soup.find_all('table')  #降水量のデータが入っているテーブルを探す
    table = tables[5]  #降水量合計が入っているテーブル（５番目）

    rows = table.find_all('tr')  #テーブルすべての行を取得する
    monthly_rain = {}  #月ごとの降水量を入れる辞書

    for row in rows:  #テーブルの行を１行ずつ処理する
        cells = row.find_all('td')  #その行のセルを全部取り出す

        if len(cells) >=2:
            month = cells[0].text.strip()  #1番目(月)のセル(cells[0])のテキストを取り出して空白を消す(strip())
            rain = cells[3].text.strip()  #2番目(降水量)のセル(cells[1])のテキストを取り出して空白を消す(strip())
            monthly_rain[month] = rain  #月をキーにして降水量を値として辞書に追加

    return monthly_rain

def main():
    all_data = {}  #全年の降水量データを入れる辞書

    for city, info in CITIES.items():  #５都市を１つずつ処理
        print(f'{city}のデータを取得中...')
    
        rain = fetch_rain(city, info['prec_no'], info['block_no'], YEAR)  #rainに都市番号と地方ナンバーと都市を指定
        
        all_data[city] = rain  #都市名をキーにして降水量データを追加   
        
        time.sleep(1)  #サーバーへの負荷を防ぐため１秒待つ

    print('取得完了！' )

    df = pd.DataFrame(all_data)  #辞書をデータフレームに変換
    
    df.to_csv('rain_data.csv', encoding='utf-8-sig')  #CSVに保存
    print('rain_data.csvに保存しました！')

if __name__ == '__main__':
    main()
