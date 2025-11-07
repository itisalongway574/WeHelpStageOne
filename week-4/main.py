from fastapi import FastAPI, Request
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

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


@app.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    if not email or not password:
        return RedirectResponse(url="/ohoh?msg=請輸入信箱和密碼", status_code=303)
    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED_IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    else:
        return RedirectResponse(url="/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)


@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("LOGGED_IN"):
        return RedirectResponse(url="/", status_code=303)
    else:
        return templates.TemplateResponse("member.html", {"request": request})


@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED_IN"] = False
    return RedirectResponse(url="/", status_code=303)


@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg: str):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg})

    # 設定伺服器的啟動路徑
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
