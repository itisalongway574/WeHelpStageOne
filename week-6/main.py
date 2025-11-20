from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import urllib.request as url_request
import json
import mysql.connector
from config import DB_CONFIG


# ================================
# 連接MySQL資料庫
# ================================
def get_db_connection():
    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )
    return connection


# ================================
# 設定後端伺服器
# ================================
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="b9178e7811b6cb5238c6e7df291ca264"
)

# 設定stactic file路徑
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定templates路徑
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/signup")
async def signup(request: Request, signup_name: str = Form(), signup_email: str = Form(), signup_password: str = Form()):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # 查詢是否有重複的 email
    cursor.execute("SELECT * FROM member WHERE email = %s", (signup_email,))
    existing_member = cursor.fetchone()

    if existing_member:
        cursor.close()
        conn.close()
        return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)
    else:
        cursor.execute("INSERT INTO member (name, email, password) VALUES (%s, %s, %s)",
                       (signup_name, signup_email, signup_password))
        conn.commit()
        cursor.close()
        conn.close()
        return RedirectResponse(url="/", status_code=303)


@app.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    # 檢查是否有輸入信箱與密碼
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)
    # 連接資料庫
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # 查詢是否有符合的信箱與密碼
    cursor.execute(
        "SELECT id, name, email FROM member WHERE email = %s AND password = %s", (email, password))
    member = cursor.fetchone()
    cursor.close()
    conn.close()
    # 根據查詢結果導向不同結果
    # 有符合的帳號密碼則登入成功
    if member:
        request.session["member_id"] = member["id"]
        request.session["member_name"] = member["name"]
        request.session["member_email"] = member["email"]
        return RedirectResponse(url="/member", status_code=303)
    # 沒有符合的帳號密碼則登入失敗
    else:
        return RedirectResponse(url="/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)


@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    # 檢查是否已經登入
    if not request.session.get("member_id"):
        return RedirectResponse(url="/", status_code=303)
    # 將會員名稱傳遞到template
    member_name = request.session.get("member_name")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # 查詢留言資料
    cursor.execute("""
    SELECT message.id, message.content, message.time, member.name, message.member_id
    FROM message
    JOIN member ON message.member_id = member.id
    ORDER BY message.time DESC
    """)
    member_messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("member.html", {
        "request": request,
        "member_name": member_name,
        "member_messages": member_messages})


@app.post("/createMessage")
async def createMessage(request: Request, content: str = Form()):
    if not content:
        return RedirectResponse(url="/ohoh?msg=請輸入留言", status_code=303)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)",
                   (request.session.get("member_id"), content))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/member", status_code=303)


@app.post("/deleteMessage")
async def deleteMessage(request: Request, message_id: int = Form()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/member", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})


@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def hotel(request: Request, hotel_id: int):
    for hotel in hotels_result:
        if hotel['hotel_id'] == hotel_id:
            return templates.TemplateResponse("hotel.html", {"request": request, "hotel": hotel})
    return templates.TemplateResponse("hotel.html", {"request": request, "hotel": None})

    # 設定伺服器的啟動路徑
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# ================================
# 處理旅館資料
# ================================
# 要抓取的網址
url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_eng = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

with url_request.urlopen(url_ch) as response:
    data_string_ch = response.read().decode("utf-8")
with url_request.urlopen(url_eng) as response:
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

hotels_result = []

for i in range(len(ordered_list_ch)):
    hotels_result.append({
        'hotel_id': ordered_list_ch[i]['_id'],
        'chinese_name': ordered_list_ch[i]['旅宿名稱'],
        'english_name': ordered_list_eng[i]['hotel name'],
        'phone': ordered_list_ch[i]['電話或手機號碼'],
    })
