rainfall_data = {
    "東京":[52, 56, 117, 125, 138, 168, 153, 168, 210, 198, 93, 51],
    "大阪":[45, 62, 104, 126, 146, 184, 157, 91, 166, 112, 69, 45],
    "札幌":[113, 94, 77, 57, 53, 46, 81, 123, 170, 109, 113, 111]
}


months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

for city, rain_list in rainfall_data.items():
    max_rain = max(rain_list)
    min_rain = min(rain_list)

    max_month_index = rain_list.index(max_rain)
    min_month_index = rain_list.index(min_rain)

    print("----", city, "----")
    print("雨が最も多い月：", months[max_month_index], f"{max_rain}mm")
    print("雨が最も少ない月：", months[min_month_index], f"{min_rain}mm")
    print()

