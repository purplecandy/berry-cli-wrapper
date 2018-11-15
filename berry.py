import json
import requests
import string
import os
import urllib.request


class Berry():
    def __init__(self):
        self.list_movies = 'https://yts.am/api/v2/list_movies.json'
        self.movies_details = 'https://yts.am/api/v2/movie_details.json'
        self.prev = ''
        self.page = 1
        self.query_term = ''
        self.path = os.getcwd()

    def responseJson(self, url):
        url_get = requests.get(url)
        json_result = url_get.json()
        if(json_result['status'] == 'ok'):
            return json_result
        else:
            print('Query not successful')

    def search_movie(self, query, limit=10):
        if(query.lower() != 'prev'):
            self.query_term = str(self.list_movies+'?query_term=' +
                                  query.replace(' ', '%') +
                                  '&limit='+str(limit))
            self.prev = self.query_term
            self.page = 1
        else:
            if(self.query_term == ''):
                print('No previous / empty query')
            else:
                self.page += 1
                self.query_term = str(self.prev + '&page=' + str(self.page))

        search_result = self.responseJson(self.query_term)
        for _dict in search_result['data']['movies']:
            print(
                f"\nTitle: {_dict['title_long']}\nId: {_dict['id']}\nImdb: {_dict['imdb_code']}\nTorrents: {len(_dict['torrents'])}")

    def movie_info(self, id):
        if type(id) == int:
            id_term = str(self.movies_details+'?movie_id='+str(id))

            data = self.responseJson(id_term)

            for key, val in data['data']['movie'].items():
                if(key in ['id', 'imdb_code', 'title', 'title_long', 'year', 'rating', 'genres', 'description_full', 'torrents']):
                    key = key.replace('_', ' ')
                    if(key == 'torrents'):
                        for _t in data['data']['movie']['torrents']:
                            print(
                                f"\nQuality : {_t['quality']} || Size: {_t['size']}")
                    else:
                        print(f'\n{key.title()} : {val}')
        else:
            print('Arg not an integer')

    def download(self, id):
        if type(id) == int:
            id_term = str(self.movies_details+'?movie_id='+str(id))
            url = self.responseJson(id_term)

            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]
            urllib.request.install_opener(opener)

            print('\nCurrent Download Directory:', self.path)
            print('\nLooking for available torrents')

            for _ in url['data']['movie']['torrents']:
                print(
                    f"\nQuality: {_['quality']} || Size: {_['size']}\n Hash: {_['date_uploaded_unix']}")

                op = input(
                    'Do you want to skip(s) or download(d) or download & skip rest(ds)').lower()

                self.path = os.getcwd() + '\\' + \
                    url['data']['movie']['title'] + \
                    ' [' + _['size'] + '] ' + '[Berry].torrent'
                if op == 's':
                    pass
                elif op == 'd':
                    file_url = _['url']
                    print(file_url)
                    urllib.request.urlretrieve(file_url, self.path)
                elif op == 'ds':
                    file_url = _['url']
                    print(file_url)
                    urllib.request.urlretrieve(file_url, self.path)
                    break
                else:
                    print('invalid input :/ continuing loop')
        else:
            print('Arg not an integer')


Req = Berry()
# Req.search_movie('the')
#print('EXECUTING PREV')
# eq.search_movie('prev')
Req.download(9540)
'''
ytapi = requests.get(
    'https://yts.am/api/v2/list_movies.json?query_term=Mile%2022')

data = ytapi.json()

print(data['status'])
'''
