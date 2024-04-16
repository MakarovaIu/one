# Вам даны идентификаторы художников в базе Artsy.
# Для каждого идентификатора получите информацию о имени художника и годе рождения.
# Выведите имена художников в порядке неубывания года рождения. В случае если у художников одинаковый год рождения,
# выведите их имена в лексикографическом порядке.

import requests
from pprint import pprint


client_id = "62f9a0824c8f1f9b2056"
client_secret = "f58c1502fe86f181139996fd0c0bc9a4"
token_url = "https://api.artsy.net/api/tokens/xapp_token"


def get_token():
    # request to get a token
    res = requests.post(token_url, data={"client_id": client_id, "client_secret": client_secret})
    ans = res.json()
    # saving the token
    token = ans["token"]
    return token


class Artists:
    def __init__(self):
        self.artist_ids = []
        self.artists_info = []
        self.token = get_token()
        # creating a header with the token
        self.headers = {"X-Xapp-Token": self.token}
        self.api_url = "https://api.artsy.net/api/artists/{}"

    def read_file(self, file):
        with open(file) as f:
            self.artist_ids = [artist.strip() for artist in f]

    def form_artists_dict(self):
        """ Forms JSON-like self.artists_info based on artists' ids provided in a file.
         Created a dict for each artist with birthday, sortable_name and id as keys. """
        for artist_id in self.artist_ids:
            r = requests.get(self.api_url.format(artist_id), headers=self.headers)
            r.encoding = 'utf-8'
            r_json = r.json()
            self.artists_info.append(
                {"birthday": r_json["birthday"], "sortable_name": r_json["sortable_name"], "id": artist_id})

    def print_sorted_artists(self):
        """ Prints out artists names sorted based on birth year (ascending).
        For artists of the same birthyear alphabetic order is used. """
        res = sorted(self.artists_info, key=lambda x: (x["birthday"], x["sortable_name"]))
        for item in res:
            print(item["sortable_name"])

    def main(self, filename):
        self.read_file(filename)
        self.form_artists_dict()
        # pprint(self.artists_info)
        self.print_sorted_artists()


if __name__ == '__main__':
    filename = "artists.txt"

    e = Artists()
    e.main(filename)
