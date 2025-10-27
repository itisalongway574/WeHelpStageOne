import urllib.request as request
import json
import csv
import os

# 要抓取的網址
url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_eng = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

with request.urlopen(url_ch) as response:
    data_string_ch = response.read().decode("utf-8")
with request.urlopen(url_eng) as response:
    data_string_eng = response.read().decode("utf-8")

# 轉換成json
data_ch = json.loads(data_string_ch)
data_eng = json.loads(data_string_eng)

# 單獨抽出裡面的list
list_ch = data_ch['list']
list_eng = data_eng['list']

# 重新排序
ordered_list_ch = sorted(list_ch, key=lambda x: x['_id'])
ordered_list_eng = sorted(list_eng, key=lambda x: x['_id'])

# 確認id都有對應正確
# for i in range(len(ordered_list_ch)):
#     if ordered_list_ch[i]['_id'] != ordered_list_eng[i]['_id']:
#         print('Not match')
#         break
#     else:
#         print('Match')

hotels_result = []

for i in range(len(ordered_list_ch)):
    hotels_result.append({
        'chinese_name': ordered_list_ch[i]['旅宿名稱'],
        'english_name': ordered_list_eng[i]['hotel name'],
        'chinese_address': ordered_list_ch[i]['地址'],
        'english_address': ordered_list_eng[i]['address'],
        'phone': ordered_list_ch[i]['電話或手機號碼'],
        'room_count': ordered_list_ch[i]['房間數'],
    })

# print(hotels_result[0])

# 定義CSV欄位名稱
hotels_csv_field=['chinese_name', 'english_name', 'chinese_address', 'english_address', 'phone', 'room_count']
hotels_csv_name='hotels.csv'

# 產生CSV檔案
with open(hotels_csv_name, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=hotels_csv_field)
    writer.writerows(hotels_result)

# 預先定義districts_result的結構
districts_result = [
    {'district': '大安區', 'hotel_count': 0,'room_count': 0},
    {'district': '大同區', 'hotel_count': 0,'room_count': 0},
    {'district': '中山區', 'hotel_count': 0,'room_count': 0},
    {'district': '中正區', 'hotel_count': 0,'room_count': 0},
    {'district': '萬華區', 'hotel_count': 0,'room_count': 0},
    {'district': '信義區', 'hotel_count': 0,'room_count': 0},
    {'district': '松山區', 'hotel_count': 0,'room_count': 0},
    {'district': '士林區', 'hotel_count': 0,'room_count': 0},
    {'district': '北投區', 'hotel_count': 0,'room_count': 0},
    {'district': '內湖區', 'hotel_count': 0,'room_count': 0},
    {'district': '南港區', 'hotel_count': 0,'room_count': 0},
    {'district': '文山區', 'hotel_count': 0,'room_count': 0},
]

# 建立一個行政區的列表用於比對
districts_names = [item['district'] for item in districts_result]

# 比對每一間飯店
for hotel in hotels_result:
    # 將選出來的飯店，去比對每一個行政區，並建立index方便對照
    for index, district_data in enumerate(districts_result):
        district_name = district_data['district']
        
        # 如果地址中有比對的行政區名稱，就代表找到對應的行政區
        if district_name in hotel['chinese_address']:
            districts_result[index]['hotel_count'] += 1
            districts_result[index]['room_count'] += int(hotel['room_count'])
            
            # 因為已經找到了，就不用繼續比對
            break

# print(districts_result)

districts_csv_field=['district', 'hotel_count', 'room_count']
districts_csv_name='districts.csv'
with open(districts_csv_name, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=districts_csv_field)
    writer.writerows(districts_result)

# 驗算總數是否吻合
# total_hotels=0
# total_rooms=0
# total_hotels_district=0
# total_rooms_district=0

# for i in range(len(districts_result)):
#     total_hotels_district += districts_result[i]['hotel_count']
#     total_rooms_district += districts_result[i]['room_count']

# for i in range(len(list_ch)):
#     total_hotels += 1
#     total_rooms += int(list_ch[i]['房間數'])

# print(f"Total hotels: {total_hotels}")
# print(f"Total rooms: {total_rooms}")
# print(f"Total hotels: {total_hotels_district}")
# print(f"Total rooms: {total_rooms_district}")





