
# 🌧️ Japan Rain Analysis

複数都市の月別降水量CSVを読み込み、統計分析・グラフ生成・結果CSV出力までを自動で行うPythonスクリプトです。

---

## 📋 機能一覧

- 都市ごとの最大・最小・平均降水量を計算
- 最も降水量が多い月・少ない月を表示
- 全都市の集計結果（最多・最少都市）を表示
- 棒グラフ・折れ線グラフ・合体グラフを自動生成・保存
- 分析結果をCSVファイルに出力（平均降水量の多い順）

---

## 🗂️ ファイル構成

```
japan-rain-analysis/
├── analyze_rain.py       # メインスクリプト
├── rainfall.csv          # 入力データ（例）
├── rainfall.png          # 出力：棒グラフ
├── line_graph.png        # 出力：折れ線グラフ
├── combined_graph.png    # 出力：合体グラフ（棒＋折れ線）
└── rainfall_result.csv   # 出力：分析結果CSV
```

---

## 📦 必要なライブラリ

```
pandas
matplotlib
```

インストールコマンド：

```bash
pip install pandas matplotlib
```

---

## 📄 入力CSVの形式

1列目に都市名、以降に月別降水量（mm）を記載します。

```csv
city,jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec
東京,52,56,117,125,138,168,153,168,210,198,93,51
大阪,45,62,104,126,146,184,157,91,166,112,69,45
札幌,113,94,77,57,53,46,81,123,170,109,113,111
```

---

## 🚀 使い方

```bash
python analyze_rain.py <CSVファイルパス>
```

### 実行例

```bash
python analyze_rain.py rainfall.csv
```

### 出力例（ターミナル）

```
 ------東京------
最大降水量： 210 mm
最小降水量： 51 mm
平均降水量： 127.8 mm
最大降水月： 9月
最小降水月： 12月

 ------集計結果------
平均降水量最多都市： 東京
平均降水量： 127.4 mm
平均降水量最小都市： 札幌
平均降水量： 95.6 mm

---

## 📊 出力ファイル

| ファイル名 | 内容 |
|---|---|
| `rainfall.png` | 都市別平均降水量の棒グラフ |
| `line_graph.png` | 都市別平均降水量の折れ線グラフ |
| `combined_graph.png` | 棒グラフ＋折れ線グラフの合体グラフ |
| `rainfall_result.csv` | 都市別分析結果（平均降水量の多い順） |

---

## 🛠️ 開発環境

- Python 3.x
- pandas
- matplotlib

---

## 👤 作者

[lucky-momo-2026](https://github.com/lucky-momo-2026)