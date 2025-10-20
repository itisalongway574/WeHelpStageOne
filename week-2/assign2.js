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
            // 檢查時間是否重疊，如果重疊了就標記為不可用，並跳出內層迴圈
            if (start < existingBooking.end && end > existingBooking.start) {
                isTimeAvailable = false;
                break;
            }
        }

        // 如果檢查完所有預約後，時間仍然可用，就把它加入候選名單
        if (isTimeAvailable) {
            availableServices.push(checkingService);
        }
    }

    // console.log(availableServices);

    if (availableServices.length === 0) {
        console.log("Sorry");
        return;
    }

    // console.log(availableServices);

    // 第二步：遞迴檢查候選名單中的service是否符合條件
    // 傳入的條件格式為「判斷元素」＋「運算符號」＋「判斷基準」
    // 判斷元素只有三種可能，r, c, name
    // 運算符有幾種可能，<, >, <=, >=, =, !=
    // 判斷基準可以為數字或字串，如果是r,c，那就會是數字；如果是name，那就會是S1,S2,S3其中之一

    let compareType = "";
    let compareOperator = "";
    let compareValue = "";

    //取出運算符，分離出判斷元素和判斷基準
    if (criteria.includes(">=")) {
        compareOperator = ">=";
    } else if (criteria.includes("<=")) {
        compareOperator = "<=";
    } else {
        compareOperator = "=";
    }

    let compareTypeAndValue = criteria.split(compareOperator);
    // console.log(compareTypeAndValue);
    compareType = compareTypeAndValue[0];
    compareValue = compareTypeAndValue[1];

    //如果compareType是name，直接比對符合的service是否存在於前面的availableServices中
    if (compareType === "name") {
        availableServices = availableServices.filter(service => service.name === compareValue);
        // 如果有符合就會print出符合的名字
        if (availableServices.length > 0) {
            console.log(availableServices[0].name);
            bookings[availableServices[0].name].push({
                start: start,
                end: end
            });
            console.log(bookings);
        } else {
            console.log("Sorry");
        }
    }
    else {
        //如果compareType是r或c，要找出運算符條件的service中，數值差距最小的那一個

        //根據運算符的種類建立對應的比較函數
        let compareFunction = (a, b) => {
            if (compareOperator === ">=") {
                return a >= b;
            } else if (compareOperator === "<=") {
                return a <= b;
            } else {
                return a == b;
            }
        };

        //判斷AvailableServices中有哪些符合運算符
        let matchOperatorServices = availableServices.filter(service => {
            if (compareType === "r") {
                return compareFunction(service.r, compareValue);
            } else if (compareType === "c") {
                return compareFunction(service.c, compareValue);
            }
        });

        // console.log(matchOperatorServices);

        let calcValue = [];

        //計算matchOperatorServices中每個service的r或c與compareValue的差值
        for (const service of matchOperatorServices) {
            if (compareType === "r") {
                calcValue.push({
                    name: service.name,
                    value: Math.abs(service.r - compareValue)
                });
            } else if (compareType === "c") {
                calcValue.push({
                    name: service.name,
                    value: Math.abs(service.c - compareValue)
                });
            }
        }
        // console.log(calcValue);

        // 找出calcValue中最小的值
        let minValue = Math.min(...calcValue.map(item => item.value));
        let minValueName = calcValue.find(item => item.value === minValue).name;
        console.log(minValueName);
        if (minValueName) {
            bookings[minValueName].push({
                start: start,
                end: end
            });
            console.log(bookings);
        } else {
            console.log("Sorry");
        }
    }

    // 第三步：將最符合service的bookings紀錄中添加本次預約紀錄 
    // if (availableServices.length > 0) {
    //     for (const service of availableServices) {
    //         bookings[service.name].push({
    //             start: start,
    //             end: end
    //         });
    //     }
    // }
    // console.table({ compareType, compareOperator, compareValue });
    // console.log(bookings);
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

func2(services, 15, 17, "c>=800"); // S3
func2(services, 11, 13, "r<=4"); // S3
func2(services, 10, 12, "name=S3"); // Sorry
func2(services, 15, 18, "r>=4.5"); // S1
func2(services, 16, 18, "r>=4"); // Sorry
func2(services, 13, 17, "name=S1"); // Sorry
func2(services, 8, 9, "c<=1500"); // S2