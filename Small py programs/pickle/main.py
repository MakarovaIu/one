import pickle
import hmac
import hashlib
import json


def create_pickle_file():
    """ Creates 'file.pickle' and writes a dict into it. """
    with open("file.pickle", "wb") as f:
        data = {5: "hello"}
        pickle.dump(data, f)


def write_secrets(true_key=True):
    """ Creates and writes into 'secrets.txt' a secret key and a signature.
    Secret key is set to 'abcd'.
    If 'true_key' is True, 'file.pickle' is used to create a signature - used for testing purposes.
    If 'true_key' is False, then signature is 'cdf'.
    """
    with open("secrets.txt", "w") as secrets, open("file.pickle", 'rb') as pfile:
        secret_key = "abcd"
        if true_key:
            pickle_raw_data = pfile.read()
            signature = hmac.new(secret_key.encode(), pickle_raw_data, hashlib.sha256).hexdigest()
            secrets.write(f"{secret_key}\n{signature}")
        else:
            secrets.write(f"{secret_key}\n{'cdf'}")


def write_answer(ans):
    with open('answer.json', 'w') as json_file:
        json.dump(ans, json_file)


def main():
    with open("file.pickle", "rb") as fp, open("secrets.txt") as secrets:
        pickle_raw_data = fp.read()
        ans = secrets.read().split('\n')
        SECRET_KEY = ans[0].strip()
        SIGNATURE_EXPECTED = ans[1].strip()
    ACTUAL_SIGNATURE = hmac.new(SECRET_KEY.encode(), pickle_raw_data, hashlib.sha256).hexdigest()
    if SIGNATURE_EXPECTED == ACTUAL_SIGNATURE:
        data = pickle.loads(pickle_raw_data)
        if type(data) is dict:
            data.update({"answer": "easy pickle"})
    else:
        data = {"answer": "not correct"}
    write_answer(data)


if __name__ == '__main__':
    # create_pickle_file()
    write_secrets(true_key=False)
    main()
