import json
from pprint import pprint
from marshmallow import Schema, fields, validate, validates, ValidationError
import re

FILE_NAME = "file_to_validate.json"


def read_data_from_file(file_name):
    with open(file_name, "r") as f:
        data = json.load(fp=f)
    return data

# 18 21
class UserSchema(Schema):
    id = fields.Int(required=True)
    login = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    password = fields.Str(required=True, validate=validate.And(validate.Length(min=3, max=50)))
    email = fields.Email()
    date = fields.Date()
    status = fields.Int(required=True, validate=validate.OneOf((1, 5, 7, 9, 14)))
    is_moderator = fields.Bool(required=False)

    class Meta:
        ordered = True
        datetimeformat = "%YYYY-%mm-%dd"

    @validates("password")
    def password_validation(self, value):
        pattern = re.compile(r"[A-Z]+")
        pattern2 = re.compile(r"\d+")
        if not (pattern.search(value) and pattern2.search(value)):
            raise ValidationError("No capital letter or digit in a password.")


def main(to_print=False):
    jsondata = read_data_from_file(FILE_NAME)
    res_list = []
    schema = UserSchema()

    for user in jsondata:
        try:
            schema.load(user)
            res_list.append("OK")
        except ValidationError as err:
            if to_print:
                print()
                pprint(user)
                pprint(err.messages)
            res_list.append("Failed")
    return res_list


if __name__ == '__main__':
    res = main(to_print=True)
    print(','.join(res))

    # for k, v in enumerate(res):
    #     print(k+1, v)
