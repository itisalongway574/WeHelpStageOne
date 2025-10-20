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
    character = None
    for char in CHARACTERS:
        if char["name"] == name:
            character = char
            break

    others = [char for char in CHARACTERS if char["name"] != name]

    # 計算距離
    others_distances = []
    for other in others:
        distance = abs(character["x"] - other["x"]) + abs(character["y"] - other["y"])
        if character["side"] != other["side"]:
            distance += 2
        others_distances.append({
            "name": other["name"],
            "distance": distance
        })

    # 從 others_distances 中取出所有距離值
    all_distances = [item["distance"] for item in others_distances]
    min_distance = min(all_distances)
    max_distance = max(all_distances)

    # 根據最小值和最大值，取出所有符合條件的角色名稱
    match_min_distance = [item["name"] for item in others_distances if item["distance"] == min_distance]
    match_max_distance = [item["name"] for item in others_distances if item["distance"] == max_distance]

    # 4. Python 的 .join() 語法是 "分隔符".join(列表)
    result_min_distance = "、".join(match_min_distance)
    result_max_distance = "、".join(match_max_distance)

    # 5. Python 用 f-string 來格式化字串
    print(f"print 最遠{result_max_distance}；最近{result_min_distance}")

print("=====Task 1=====")
func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")