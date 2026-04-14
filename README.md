# 🌧️ Japan Rain Analysis

複数都市の月別降水量CSVを読み込み、統計分析・異常値検出・前年比計算・グラフ生成・結果CSV出力までを自動で行うPythonスクリプトです。
気象庁の公開データをスクレイピングで取得し、実データで分析しています。

📋 機能一覧

* 都市ごとの最大・最小・平均降水量を計算
* 最も降水量が多い月・少ない月を表示
* 標準偏差ベースの異常値検出（平均＋1.5σ超を異常値として判定）
* 前年比（mm）・前年比（%）を自動計算
* 全都市の集計結果（最多・最少都市）を表示
* 棒グラフ・折れ線グラフ・合体グラフを自動生成・保存
* 分析結果をCSVファイルに出力（順位・評価ランク付き）
* 都市名・ソートキーをコマンドライン引数で指定可能
* 複数年のデータに対応（年・都市名をCSVから自動取得）


## 🗂️ ファイル構成

```text
japan-rain-analysis/
├── analyze_rain.py       # メインスクリプト（分析・出力）
├── fetch_rain.py         # 気象庁スクレイピングスクリプト
├── rainfall_result.csv   # 出力：分析結果CSV（順位・評価・前年比付き）
└── reports/
    ├── rainfall_compare.png  # 出力：比較グラフ（棒＋折れ線）
    └── rainfall_combo.png    # 出力：合体グラフ（棒＋折れ線）
```
---

## 📦 必要なライブラリ

```
pip install pandas matplotlib requests beautifulsoup4
```
---

## 🚀 使い方

データ取得（気象庁スクレイピング）
```bash
python fetch_rain.py
```

分析実行

全都市を分析
```bash
python analyze_rain.py rain_data.csv
```

都市を絞り込んで分析
```bash
python analyze_rain.py rain_data.csv 札幌
python analyze_rain.py rain_data.csv 札幌 東京
```

ソートキーを指定して分析
```bash
python analyze_rain.py rain_data.csv --sort 前年比
python analyze_rain.py rain_data.csv --sort 平均降水量
python analyze_rain.py rain_data.csv --sort 最大降水量
python analyze_rain.py rain_data.csv --sort 前年比率
```

絞り込み＋ソートの組み合わせ
```bash
python analyze_rain.py rain_data.csv 札幌 東京 --sort 前年比
```

## 📄 入力CSVの形式
1列目に「都市名_年」、2列目以降に月別降水量（mm）を記載します。

```csv
月,1,2,3,4,5,6,7,8,9,10,11,12
札幌_2022,71.5,104.0,35.5,61.0,21.5,133.5,61.5,69.5,146.0,88.5,126.5,47.0
札幌_2023,71.5,104.0,35.5,61.0,21.5,133.5,61.5,69.5,146.0,88.5,126.5,47.0
札幌_2024,153.5,117.0,67.5,34.5,40.0,38.0,144.0,102.5,74.5,160.0,134.0,54.5
```
※fetch_rain.py を実行すると rain_data.csv が自動生成されます。

---

## 📊 出力例（ターミナル）

```text
 ------札幌_2023------
最大降水量： 146.0 mm
最小降水量： 21.5 mm
平均降水量： 80.5 mm
最大降水月： 9月
最小降水月： 5月
☔異常値あり：9月 146.0mm

 ------集計結果------
平均降水量最多都市： 福岡_2024
平均降水量： 164.2 mm
平均降水量最小都市： 札幌_2023
平均降水量： 80.5 mm
```
---

## 📊 出力ファイル

| ファイル名 | 内容 |
|---|---|
| `rainfall_result.csv` | 都市別分析結果（順位・評価・前年比付き） |
| `reports/rainfall_compare.png` | 都市別平均降水量の比較グラフ |
| `reports/rainfall_combo.png` | 棒グラフ＋折れ線グラフの合体グラフ |
---

## 💡 工夫したポイント
1. 都市・年をCSVから自動取得
都市名と年をハードコードせず、読み込んだCSVのインデックスから自動取得しています。これにより年数や都市数が変わっても修正不要で動作します。

2. 都市をまたいだ前年比の誤計算を防ぐ
shift(1) で前の行を取得する際、都市が変わるタイミングで誤計算が起きる問題がありました。groupby を使って都市ごとにグループ化してから shift(1) することで正確な前年比を計算しています。

3. コマンドライン引数の設計
--sort オプションと都市名の絞り込みを同時に指定できるよう、引数を分離して処理しています。

---

## 🛠️ 開発環境

* Python 3.14
* pandas
* matplotlib
* requests
* beautifulsoup4

---

## 👤 作者
lucky-momo-2026