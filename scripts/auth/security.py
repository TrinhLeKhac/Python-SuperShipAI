from datetime import datetime
from typing import Any, Dict, List

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from config import settings
from fastapi.responses import JSONResponse

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, settings.SECRET_KEY,
                             algorithms=[settings.SECURITY_ALGORITHM])
        if payload.get('exp') < int(datetime.now().strftime("%Y%m%d%H%M%S")):
            raise HTTPException(status_code=403, detail="Token expired")

        return payload.get('username')

    except(jwt.PyJWTError, ValidationError):
        content = {"error": True, "message": "Wrong token", "data": []}
        raise HTTPException(
            status_code=403,
            detail=content,
        )
