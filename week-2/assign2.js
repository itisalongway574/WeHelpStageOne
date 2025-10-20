// ===============================================
// Task 1
// ===============================================

const Characters = [
    {
        name: "悟空",
        x: 0,
        y: 0,
        side: "left",
    },
    {
        name: "辛巴",
        x: -3,
        y: 3,
        side: "left"
    },
    {
        name: "貝吉塔",
        x: -4,
        y: -1,
        side: "left"
    },
    {
        name: "特南克斯",
        x: 1,
        y: -2,
        side: "left"
    },
    {
        name: "丁滿",
        x: -1,
        y: 4,
        side: "right"
    },
    {
        name: "弗利沙",
        x: 4,
        y: -1,
        side: "right"
    }
]

function func1(name) {
    const character = Characters.find(character => character.name === name);
    const others = Characters.filter(character => character.name !== name);

    // 計算角色之間的距離，返回一個新陣列
    const othersDistances = others.map(other => {
        let distance = Math.abs(character.x - other.x) + Math.abs(character.y - other.y);
        if (character.side !== other.side) {
            distance += 2;
        }
        return {
            name: other.name,
            distance: distance
        };
    });

    // 根據OtherDistances陣列，取出所有距離值，並抓出最大值和最小值
    const allDistances = othersDistances.map(item => item.distance);
    const minDistance = Math.min(...allDistances);
    const maxDistance = Math.max(...allDistances);

    // 根據最小值和最大值，取出所有距離值為最小值和最大值的角色名稱
    const matchMinDistance = othersDistances.filter(item => item.distance === minDistance).map(item => item.name);
    const matchMaxDistance = othersDistances.filter(item => item.distance === maxDistance).map(item => item.name);

    const resultMinDistance = matchMinDistance.join("、");
    const resultMaxDistance = matchMaxDistance.join("、");

    // 題目要求的輸出格式有些微不同
    console.log(`print 最遠${resultMaxDistance}；最近${resultMinDistance}`);
}

console.log("=====Task 1=====");
func1("辛巴");
func1("悟空");
func1("弗利沙");
func1("特南克斯");


// ===============================================
// Task 2
// ===============================================

