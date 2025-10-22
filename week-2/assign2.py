# Task 1

CHARACTERS = [
    {
        "name": "悟空",
        "x": 0,
        "y": 0,
        "side": "left",
    },
    {
        "name": "辛巴",
        "x": -3,
        "y": 3,
        "side": "left"
    },
    {
        "name": "貝吉塔",
        "x": -4,
        "y": -1,
        "side": "left"
    },
    {
        "name": "特南克斯",
        "x": 1,
        "y": -2,
        "side": "left"
    },
    {
        "name": "丁滿",
        "x": -1,
        "y": 4,
        "side": "right"
    },
    {
        "name": "弗利沙",
        "x": 4,
        "y": -1,
        "side": "right"
    }
]

def func1(name):
    # 用character來儲存name對應的角色，在Python中要先賦予None
    character = None
    for char in CHARACTERS:
        if char["name"] == name:
            character = char
            break

    # 用others來儲存其他角色
    others = [char for char in CHARACTERS if char["name"] != name]

    # 計算角色之間的距離，返回一個新陣列
    others_distances = []
    for other in others:
        distance = abs(character["x"] - other["x"]) + abs(character["y"] - other["y"])
        if character["side"] != other["side"]:
            distance += 2
        others_distances.append({
            "name": other["name"],
            "distance": distance
        })

    # 根據OtherDistances陣列，取出所有距離值，並抓出最大值和最小值
    # python中的變數命名慣例是snake_case
    all_distances = [item["distance"] for item in others_distances]
    min_distance = min(all_distances)
    max_distance = max(all_distances)

    # 根據最小值和最大值，取出所有符合條件的角色名稱
    match_min_distance = [item["name"] for item in others_distances if item["distance"] == min_distance]
    match_max_distance = [item["name"] for item in others_distances if item["distance"] == max_distance]

    result_min_distance = "、".join(match_min_distance)
    result_max_distance = "、".join(match_max_distance)

    print(f"print 最遠{result_max_distance}；最近{result_min_distance}")

print("=====Task 1=====")
func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")


# ===============================================
# Task 2
# ===============================================

# 用來記錄已經被安排的時間
bookings = {
    "S1": [],
    "S2": [],
    "S3": []
}

# 根據指定的預約時間，去和已經安排的時間做比對
def func2(ss, start, end, criteria):
    # 第一步：確認是否有可以被預約的時段
    # 比對方式：新的預約要在S1-S3的所有既有的預約開始之前結束，或是在既有的預約結束之後開始

    available_services = []

    # 檢查傳入的services陣列裡面的每一個services的時間是否符合
    for checking_service in ss:
        is_time_available = True

        # 檢查這個服務的所有已預約紀錄
        for existing_booking in bookings[checking_service["name"]]:
            exist_start = existing_booking["start"]
            exist_end = existing_booking["end"]

            # 檢查時間是否重疊，如果重疊了就標記為不可用，然後就中斷迴圈
            if start < exist_end and end > exist_start:
                is_time_available = False
                break

        # 如果檢查完所有預約後，時間仍然可用，就把它加入候選名單
        if is_time_available:
            available_services.append(checking_service)

    # 如果沒有可用服務，就印出Sorry並中斷
    if len(available_services) == 0:
        print("Sorry")
        return

    # 第二步：從AvailableServices中找出符合條件的服務
    # 將原本傳入的條件解構成「判斷元素」、「運算符」、「判斷基準」
    compare_type = ""
    compare_operator = ""
    compare_value = None # python中要先賦予None

    #取出運算符，分離出判斷元素和判斷基準
    if ">=" in criteria:
        compare_operator = ">="
    elif "<=" in criteria:
        compare_operator = "<="
    else:
        compare_operator = "="

    # 以運算符為界線，拆分出「判斷元素」和「判斷基準」
    compare_type_and_value = criteria.split(compare_operator)
    compare_type = compare_type_and_value[0]
    # 因為拆解出來的「判斷基準」可能是字串，所以需要先轉換成數字
    value_str = compare_type_and_value[1]

    # 如果判斷元素是name，則去除前後的雙引號
    if compare_type == "name":
        compare_value = value_str.replace('"', '')
    else:
        # 如果判斷元素是r或c，則轉換成數字
        compare_value = float(value_str)


    # 如果判斷元素是name，則直接在availableServices中找出符合條件的服務
    if compare_type == "name":
        match_service = None
        for service in available_services:
            if service["name"] == compare_value:
                match_service = service
                break

        # 如果找到符合條件的服務，就印出服務名稱並更新bookings
        if match_service:
            print(match_service["name"]) 
            bookings[match_service["name"]].append({
                "start": start,
                "end": end
            })
        # 如果沒有找到符合條件的服務，就印出Sorry並中斷
        else:
            print("Sorry")
        return

    # 如果判斷元素是r或c，則在availableServices中找出符合條件的服務後，找出最接近的那一個
    else:
        # 根據運算符的種類建立對應的比較函數 (只處理 >= 和 <=)
        def compare_function(a, b):
            if compare_operator == ">=":
                return a >= b
            elif compare_operator == "<=":
                return a <= b
            return False

        # 篩選出符合運算符的服務
        match_service = [service for service in available_services if compare_function(service[compare_type], compare_value)]

        # 如果沒有合格服務，則印出 Sorry
        if len(match_service) == 0:
            print("Sorry")
            return
        # 如果只有一個符合，那就是配對結果
        elif len(match_service) == 1:
            best_match = match_service[0]
            print(best_match["name"])
            bookings[best_match["name"]].append({"start": start, "end": end})
            return

        # 如果有多個符合，用排序找出最接近的值
        else:
            #如果條件是>=，要找最小值
            if compare_operator == ">=":
                match_service.sort(key=lambda x: x[compare_type])
            #如果條件是<=，要找最大值
            elif compare_operator == "<=":
                match_service.sort(key=lambda x: x[compare_type], reverse=True)

            # 重新排序後的第一個就是最符合的結果
            best_match = match_service[0]

        # print出結果並更新bookings
        print(best_match["name"])
        bookings[best_match["name"]].append({"start": start, "end": end})


services = [
    {
        "name": "S1",
        "r": 4.5,
        "c": 1000
    },
    {
        "name": "S2",
        "r": 3,
        "c": 1200
    },
    {
        "name": "S3",
        "r": 3.8,
        "c": 800
    }
]

print("=====Task 2=====")
func2(services, 15, 17, "c>=800") # S3
func2(services, 11, 13, "r<=4") # S3
func2(services, 10, 12, "name=S3") # Sorry
func2(services, 15, 18, "r>=4.5") # S1
func2(services, 16, 18, "r>=4") # Sorry
func2(services, 13, 17, "name=S1") # Sorry
func2(services, 8, 9, "c<=1500") # S2


# ===============================================
# Task 3
# ===============================================


def func3(index):
    # 觀察數列規律，每4個為一次循環
    # 每次循環會是-2
    # 第一個項目是-2，第二個項目是-3，第三個項目是+1，第四個項目是+2
    begin_number = 25
    target_number = None
    quotient = None


    # index被4除時，餘數可能是0,1,2,3
    # 分別列舉各種餘數情況
    #如果餘數為0，就根據他經歷幾次循環去*-2
    if index % 4 == 0:
        quotient = index // 4
        target_number = begin_number - quotient * 2 - 2
    #如果餘數為1，就是(循環*-2)-2
    elif (index - 1) % 4 == 0:
        quotient = (index - 1) // 4
        target_number = begin_number - quotient * 2 - 2
    #如果餘數為2，就是(循環*-2)-2-3
    elif (index - 2) % 4 == 0:
        quotient = (index - 2) // 4
        target_number = begin_number - quotient * 2 - 5
    #如果餘數為3，就是(循環*-2)-2-3+1
    elif (index - 3) % 4 == 0:
        quotient = (index - 3) // 4
        target_number = begin_number - quotient * 2 - 4

    print("print " + str(target_number))


print("=====Task 3=====")
func3(1) # print 23
func3(5) # print 21
func3(10) # print 16
func3(30) # print 6

# ===============================================
# Task 4
# ===============================================



def func4(sp, stat, n):

    #將stat拆分成單獨的數字
    stat_array = list(stat)
    # print(stat_array)

    #建立一個陣列紀錄傳入的sp和對應的stat和原始Index
    sp_and_stat_and_orginal_inex = []
    for i in range(len(sp)):
        sp_and_stat_and_orginal_inex.append({
            "originalIndex": i,
            "sp": sp[i],
            "stat": stat_array[i],
        })
    # print(sp_and_stat_and_orginal_inex)

    #將stat是1的情況直接排除
    sp_and_stat_and_orginal_inex = [item for item in sp_and_stat_and_orginal_inex if item["stat"] != "1"]
    # print(sp_and_stat_and_orginal_inex)

    #找出SpAndStatAndOrginalInex中，sp>=n的項目
    match_sp = [item for item in sp_and_stat_and_orginal_inex if item["sp"] >= n]
    # print(match_sp)

    #如果matchSp的長度為0，那就回頭找出spAndStatAndOrginalInex中最大的值對應的OriginalIndex
    if len(match_sp) == 0:
        max_sp = max([item["sp"] for item in sp_and_stat_and_orginal_inex])
        max_sp_index = next(i for i, item in enumerate(sp_and_stat_and_orginal_inex) if item["sp"] == max_sp)
        print("print " + str(sp_and_stat_and_orginal_inex[max_sp_index]["originalIndex"]))
    #如果matchSp的長度為1，那就回頭找出spAndStatAndOrginalInex中最小的值對應的OriginalIndex
    else:
        min_sp = min([item["sp"] for item in match_sp])
        min_sp_index = next(i for i, item in enumerate(match_sp) if item["sp"] == min_sp)
        print("print " + str(match_sp[min_sp_index]["originalIndex"]))

print("=====Task 4=====")
func4([3, 1, 5, 4, 3, 2], "101000", 2) #print 5
func4([1, 0, 5, 1, 3], "10100", 4) #print 4
func4([4, 6, 5, 8], "1000", 4) #print 2
