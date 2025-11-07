from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# 設定stactic file路徑
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定templates路徑
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(email: str = Form(), password: str = Form()):
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)
    if email == "abc@abc.com" and password == "abc":
        return RedirectResponse(url="/member", status_code=303)
    else:
        return RedirectResponse(url="/ohoh?msg=信箱或密碼不正確", status_code=303)


@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    return templates.TemplateResponse("member.html", {"request": request})


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})

    # 設定伺服器的啟動路徑
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
