from scripts.api import authen, order, result, zns, output
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request, status
from ast import literal_eval
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import jwt
from typing import Union


app = FastAPI(
    title="API SUPERSHIP",
    description="There are APIs getting calculation result from history transactions of SUPERSHIP",
    docs_url="/"
)


def create_str_err(exc_str):
    errs = literal_eval(exc_str)
    res = []
    for err in errs:
        s = str(err["loc"]) + " => " + err["msg"]
        res.append(s)
    return "; ".join(res)


# @app.exception_handler(ValidationError)
# def wrong_authenticated_exception_handler(request: Request, exc: ValidationError):
#     content = {"error": True, "message": "Wrong token", "data": []}
#     return JSONResponse(content=content, status_code=status.HTTP_403_FORBIDDEN)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    path = request.url.path
    # print(path)
    if path == "/superai/auth":
        content = {"error": True, "message": create_str_err(exc_str), "data": {"token": "Invalid"}}
    else:
        content = {"error": True, "message": create_str_err(exc_str), "data": []}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


app.include_router(authen.router, tags=[""], prefix="/superai/auth")
app.include_router(zns.router, tags=[""], prefix="/superai/zns")
app.include_router(order.router, tags=[""], prefix="/superai/order")
app.include_router(result.router, tags=[""], prefix="/superai/result")
app.include_router(output.router, tags=[""], prefix="/superai/output")
