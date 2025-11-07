from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import mysql.connector
from mysql.connector import pooling

# --- Pydantic 模型 (根據投影片規格) ---
class Message(BaseModel):
    author: str
    content: str

# --- 資料庫連線池設定 ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "MySQL_wadejin1996", # 請替換成您自己的密碼
    "database": "fastapi"
}
try:
    connection_pool = pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=5, **db_config)
    print("資料庫連線池建立成功。")
except Exception as e:
    print(f"資料庫連線池建立失敗: {e}")
    connection_pool = None

app = FastAPI()

# --- API 路由 (根據投影片規格) ---

# 新增留言的API
@app.post("/api/message")
def create_message(message: Message):
    if not connection_pool:
        raise HTTPException(status_code=500, detail="資料庫連線失敗")

    con = None
    cursor = None
    try:
        con = connection_pool.get_connection()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO message(author, content) VALUES (%s, %s)", 
            (message.author, message.content)
        )
        con.commit()
        return {"message": "留言新增成功"}
    except Exception as e:
        print(f"新增留言時發生錯誤: {e}")
        if con:
            con.rollback()
        raise HTTPException(status_code=500, detail="伺服器內部錯誤，無法新增留言")
    finally:
        if cursor:
            cursor.close()
        if con and con.is_connected():
            con.close()

# --- 掛載靜態檔案 ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")