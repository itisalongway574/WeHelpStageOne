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

// 用來記錄已經被安排的時間
let bookings =
{
    "S1": [],
    "S2": [],
    "S3": []
}

// 根據指定的預約時間，去和已經安排的時間做比對
function func2(ss, start, end, criteria) {
    // 第一步：確認是否有可以被預約的時段
    // 比對方式：新的預約要在S1-S3的所有既有的預約開始之前結束，或是在既有的預約結束之後開始

    let availableServices = [];

    // 檢查傳入的services陣列裡面的每一個services的時間是否符合
    for (const checkingService of ss) {
        let isTimeAvailable = true;

        // 檢查這個服務的所有已預約紀錄
        for (const existingBooking of bookings[checkingService.name]) {
            const existStart = existingBooking.start;
            const existEnd = existingBooking.end;

            // 檢查時間是否重疊，如果重疊了就標記為不可用，並跳出內層迴圈
            if (start < existEnd && end > existStart) {
                isTimeAvailable = false;
                break;
            }
        }

        // 如果檢查完所有預約後，時間仍然可用，就把它加入候選名單
        if (isTimeAvailable) {
            availableServices.push(checkingService);
        }
    }

    if (availableServices.length === 0) {
        console.log("Sorry");
        return;
    }

    // 第二步：從AvailableServices中找出符合條件的服務
    // 將原本傳入的條件解構成「判斷元素」、「運算符」、「判斷基準」
    let compareType = "";
    let compareOperator = "";
    let compareValue;

    //取出運算符，分離出判斷元素和判斷基準
    if (criteria.includes(">=")) {
        compareOperator = ">=";
    } else if (criteria.includes("<=")) {
        compareOperator = "<=";
    } else {
        compareOperator = "=";
    }

    // 以運算符為界線，拆分出「判斷元素」和「判斷基準」
    let compareTypeAndValue = criteria.split(compareOperator);
    compareType = compareTypeAndValue[0];
    // 因為拆解出來的「判斷基準」可能是字串，所以需要先轉換成數字
    let valueStr = compareTypeAndValue[1];

    // 如果判斷元素是name，則去除前後的雙引號
    if (compareType === "name") {
        compareValue = valueStr.replace(/"/g, '');
    } else {
        // 如果判斷元素是r或c，則轉換成數字
        compareValue = parseFloat(valueStr);
    }


    // 如果判斷元素是name，則直接在availableServices中找出符合條件的服務
    if (compareType === "name") {
        const matchService = availableServices.find(service => service.name === compareValue);

        if (matchService) {
            console.log(matchService.name);
            // 第三步：將最符合service的bookings紀錄中添加本次預約紀錄 
            bookings[matchService.name].push({
                start: start,
                end: end
            });
        } else {
            // 時間可用，但條件不符
            console.log("Sorry");
        }
        return;
    }

    // 如果判斷元素是r或c，則在availableServices中找出符合條件的服務後，找出最接近的那一個
    else {
        // 根據運算符的種類建立對應的比較函數 (只處理 >= 和 <=)
        let compareFunction = (a, b) => {
            if (compareOperator === ">=") {
                return a >= b;
            } else if (compareOperator === "<=") {
                return a <= b;
            }
            return false;
        };

        // 篩選出符合運算符的服務
        let matchService = availableServices.filter(service => {
            const serviceValue = service[compareType];
            return compareFunction(serviceValue, compareValue);
        });

        let bestMatch;
        // 如果沒有合格服務，則印出 Sorry
        if (matchService.length === 0) {
            console.log("Sorry");
            return;
        }
        // 如果只有一個符合，那就是配對結果
        else if (matchService.length === 1) {
            bestMatch = matchService[0];
            console.log(bestMatch.name);
            bookings[bestMatch.name].push({ start: start, end: end });
            return;

        }
        // 如果有多個符合，用排序找出最接近的值
        else {
            matchService.sort((a, b) => {
                //如果條件是>=，要找最小值
                if (compareOperator === ">=") {
                    return a[compareType] - b[compareType];
                }
                //如果條件是<=，要找最大值
                else if (compareOperator === "<=") {
                    return b[compareType] - a[compareType];
                }
            });

            // 重新排序後的第一個就是最符合的結果
            bestMatch = matchService[0];
        }

        // print出結果並更新bookings
        console.log(bestMatch.name);
        bookings[bestMatch.name].push({ start: start, end: end });
    }
}


const services = [
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
];

console.log("=====Task 2=====");
func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2


// ===============================================
// Task 3
// ===============================================


function func3(index) {
    // 觀察數列規律，每4個為一次循環
    // 每次循環會是-2
    // 第一個項目是-2，第二個項目是-3，第三個項目是+1，第四個項目是+2
    let beginNumber = 25;
    let targetNumber;
    let quotient;


    // index被4除時，餘數可能是0,1,2,3
    // 分別列舉各種餘數情況
    //如果餘數為0，就根據他經歷幾次循環去*-2
    if (index / 4 === 0) {
        quotient = index / 4;
        targetNumber = beginNumber - quotient * 2;
    }
    //如果餘數為1，就是(循環*-2)-2
    else if ((index - 1) % 4 === 0) {
        quotient = (index - 1) / 4;
        targetNumber = beginNumber - quotient * 2 - 2;
    }
    //如果餘數為2，就是(循環*-2)-2-3
    else if ((index - 2) % 4 === 0) {
        quotient = (index - 2) / 4;
        targetNumber = beginNumber - quotient * 2 - 5;
    }
    //如果餘數為3，就是(循環*-2)-2-3+1
    else if ((index - 3) % 4 === 0) {
        quotient = (index - 3) / 4;
        targetNumber = beginNumber - quotient * 2 - 4;
    }

    console.log("print " + targetNumber);

}

console.log("=====Task 3=====");
func3(1); // print 23
func3(5); // print 21
func3(10); // print 16
func3(30); // print 6

// ===============================================
// Task 4
// ===============================================



function func4(sp, stat, n) {

    //將stat拆分成單獨的數字
    let statArray = stat.split("");
    // console.log(statArray);

    //建立一個陣列紀錄傳入的sp和對應的stat和原始Index
    let spAndStatAndOrginalInex = [];
    for (let i = 0; i < sp.length; i++) {
        spAndStatAndOrginalInex.push({
            originalIndex: i,
            sp: sp[i],
            stat: statArray[i],
        });
    }
    // console.log(spAndStatAndOrginalInex);

    //將stat是1的情況直接排除
    spAndStatAndOrginalInex = spAndStatAndOrginalInex.filter(item => item.stat !== "1");
    // console.log(spAndStatAndOrginalInex);

    //找出SpAndStatAndOrginalInex中，sp>=n的項目
    let matchSp = spAndStatAndOrginalInex.filter(item => item.sp >= n);
    // console.log(matchSp);

    //如果matchSp的長度為0，那就回頭找出spAndStatAndOrginalInex中最大的值對應的OriginalIndex
    if (matchSp.length === 0) {
        let maxSp = Math.max(...spAndStatAndOrginalInex.map(item => item.sp));
        let maxSpIndex = spAndStatAndOrginalInex.findIndex(item => item.sp === maxSp);
        console.log("print " + spAndStatAndOrginalInex[maxSpIndex].originalIndex);
    }
    //如果matchSp的長度為1，那就回頭找出spAndStatAndOrginalInex中最小的值對應的OriginalIndex
    else {
        let minSp = Math.min(...matchSp.map(item => item.sp));
        let minSpIndex = matchSp.findIndex(item => item.sp === minSp);
        console.log("print " + matchSp[minSpIndex].originalIndex);
    }
}
console.log("=====Task 4=====");
func4([3, 1, 5, 4, 3, 2], "101000", 2); //print 5
func4([1, 0, 5, 1, 3], "10100", 4); //print 4
func4([4, 6, 5, 8], "1000", 4); //print 2