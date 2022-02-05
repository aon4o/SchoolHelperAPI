from typing import List, Optional

from pydantic import BaseModel


# CLASSES
class SubjectBase(BaseModel):
    guild_id: str
    name: str


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    
    class Config:
        orm_mode = True


# CHANNEL CATEGORIES
class GuildCategoryBase(BaseModel):
    guild_id: str
    category_id: str


class GuildCategoryCreate(GuildCategoryBase):
    pass


class GuildCategory(GuildCategoryBase):
    id: int
    
    class Config:
        orm_mode = True


# USERS
class UserBase(BaseModel):
    guild_id = str
    username = str
    email = str
    first_name = str
    last_name = str


class UserCreate(UserBase):
    password = str


class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# OAuth2
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    email: str = None


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                from fastapi import HTTPException
                from starlette.status import HTTP_403_FORBIDDEN
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param



