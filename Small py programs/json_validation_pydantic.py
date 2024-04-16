import json
from pprint import pprint
import re
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, validator, ValidationError

FILE_NAME = "file_to_validate.json"


def read_data_from_file(file_name):
    with open(file_name, "r") as f:
        data = json.load(fp=f)
    return data


class User(BaseModel):
    id: int
    login: str
    password: str
    email: EmailStr | None
    date: date | None
    status: int
    is_moderator: bool | None

    @validator('login')
    def login_length(cls, val):
        if 3 <= len(val) <= 20:
            return val
        raise ValidationError("Login must be min 3 and max 20 symbols.")

    @validator('password')
    def symbols_in_password(cls, val):
        pattern = re.compile(r"[A-Z]+")
        pattern2 = re.compile(r"\d+")
        if pattern.search(val) and pattern2.search(val):
            return val
        raise ValidationError("No capital letters or digits in a password.")

    @validator('password')
    def password_length(cls, val):
        if 3 <= len(val) <= 50:
            return val
        raise ValidationError("Password length must be min 3, max 50.")

    @validator('date', pre=True)
    def parse_date(cls, val):
        return datetime.strptime(val, "%Y-%m-%d").date()

    @validator('status')
    def valid_status_code(cls, val):
        if int(val) in (1, 5, 7, 9, 14):
            return val
        raise ValidationError("Status must be one of: (1, 5, 7, 9, 14)")

    class Config:
        extra = 'forbid'


def main(to_print=False):
    jsondata = read_data_from_file(FILE_NAME)
    res_list = []

    for user in jsondata:
        try:
            User(**user)
            res_list.append("OK")
        except ValidationError as err:
            if to_print:
                print()
                pprint(user)
                pprint(err)
            res_list.append("Failed")
    return res_list


if __name__ == '__main__':
    res = main(to_print=True)
    print(','.join(res))
