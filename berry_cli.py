import json
import requests
import string
import os
import urllib.request
import cmd
import sys

sys.tracebacklimit = 0


class Berry(cmd.Cmd):
    def __init__(self):
        self.list_movies = 'https://yts.am/api/v2/list_movies.json'
        self.movies_details = 'https://yts.am/api/v2/movie_details.json'
        self.prev = ''
        self.page = 1
        self.query_term = ''
        self.path = os.getcwd()

        super(Berry, self).__init__()

    def do_download(self, id):
        """
        download id
        Download command let's you download torrents
        Example: download 7540

            * The id only accepts numbers, if you don't have the id please search the movie first, obtain the id and then search for download with the id

        """
        if(len(id) != 0):
            try:
                id = int(id)
            except ValueError:
                print('ID value is a number/integer')
            else:
                self.download(id)
        else:
            print('You need to specify the id')

    def do_search(self, query):
        """
        Search movie 
        Example: search The lord of the rings
        Options: 
            --limit=int
            [By default the search will show 10 results, if limit=15 it will show 15 instead of 10]
            *make sure there is no space at the end
        Example: search The lord of the rings--limit=10
        """
        if(len(query) != 0 and len(query) > 3):
            try:
                arr = query.split('--limit=', 2)
                key = arr[0]
                limit = arr[1]
            except IndexError:
                self.search_movie(key)
            else:
                print('No erros', key, limit)
                self.search_movie(key, limit)
        elif(query == 'prev'):
            self.search_movie('prev')

        else:
            print('Empty/Invalid search or search query too small')

    def do_movieinfo(self, id):
        """
        movieinfo id
        This command will give you the complete information about the movie such as Title,Release Year,Description,Genre,Torrents,Cast etc
        Example: movieinfo 9540
            * The id only accepts numbers
            * The id can be used to download movies torrents
        """
        if(len(id) != 0):
            try:
                id = int(id)
            except ValueError:
                print('ID value is a number/integer')

            else:
                self.movie_info(id)

        else:
            print('Empty/Invalid ID')

    def do_quit(self, args):
        """
        Quits the program.
        """
        print("Quitting.")
        raise SystemExit

    def responseJson(self, url):
        # Making a request
        try:
            url_get = requests.get(url, timeout=60)

            # Deconding the json
            json_result = url_get.json()

            # make sure if the status return is successful
        except ConnectionError:
            print('No internet connetion, internet connection is require')
        except TimeoutError:
            print('Process took too long to execute.....terminated. Please try again.')
        except:
            print('HTTP Exception erros :/')
        else:
            if(json_result['status'] == 'ok'):
                return json_result
            else:
                print('Query not successful')

    def search_movie(self, query, limit=10):
        # If the query is prev then execute else block otherwise if block
        try:
            if(query.lower() != 'prev'):
                self.query_term = str(self.list_movies+'?query_term=' +
                                      query.replace(' ', '%') +
                                      '&limit='+str(limit))
                # Setting prev and page 1
                self.prev = self.query_term
                self.page = 1
            else:
                if(self.query_term == ''):
                    print('No previous / empty query')
                else:
                    # Query is prev hence page++ and concatination
                    self.page += 1
                    print(f'\n\tSEARCH PAGE', self.page)
                    self.query_term = str(
                        self.prev + '&page=' + str(self.page))

            # Once the query_term is generated we can proceed to make a request
            search_result = self.responseJson(self.query_term)
            for _dict in search_result['data']['movies']:
                print(
                    f"\t\nTitle: {_dict['title_long']}\nId: {_dict['id']}\nImdb: {_dict['imdb_code']}\nTorrents: {len(_dict['torrents'])}")

        except:
            print('Search Error')

    def movie_info(self, id):
        # Requesting an ID and converting string input to int type
        try:
            if type(id) == int:
                id_term = str(self.movies_details+'?movie_id='+str(id))

                data = self.responseJson(id_term)

                # Loops inside data>movie then loops inside movie>torrents

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
        except:
            print('Movie Info Error')

    def download(self, id):
        # Requesting ID and converting str input to int type
        try:
            if type(id) == int:
                id_term = str(self.movies_details+'?movie_id='+str(id))
                url = self.responseJson(id_term)

                # Creating fake headers and file openes from built in functions from urllid to download
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')]
                urllib.request.install_opener(opener)

                print('\nCurrent Download Directory:', self.path)
                print('\nLooking for available torrents')

                # looping thorugh json data>movie>torrents
                for _ in url['data']['movie']['torrents']:
                    print(
                        f"\nQuality: {_['quality']} || Size: {_['size']}\nSeeds: {_['seeds']} || Peers: {_['peers']}")

                    op = input(
                        'Do you want to skip(s) or download(d) or download & skip rest(ds) [Type break to exit]').lower()

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

                    elif op == 'break':
                        print('All download skipped')
                        break
                    else:
                        print('invalid input :/ continuing loop')
            else:
                print('Arg not an integer')
        except:
            print('Download Error Exception')


if __name__ == '__main__':
    Req = Berry()
    Req.prompt = '(berry)> '
    Req.cmdloop('''
    Starting prompt...
    Welcome to Berry CLI based movie torrent downloader

    You can search, download a movie.

    Avialable Commands:
    
    download

    movieinfo

    search

    TYPE: help <command name>
    to know about commands
    ''')
