required = set(input().split())
optional = set(input().split())
user_data = set(input().split())


def check_user_data(req, opt, data):
    check = set()
    check.add(True) if req.issubset(data) else check.add(False)
    check.add(True) if (data - req).issubset(opt) else check.add(False)
    return check


if __name__ == '__main__':
    res = check_user_data(required, optional, user_data)
    print('False' if False in res else 'True')
