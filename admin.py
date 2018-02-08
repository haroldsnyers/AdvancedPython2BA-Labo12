import json
from urllib.request import urlopen

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


def loaddatatv():
    """Calls the function getlinktv from server.py and returns a list with all the data about the tv shows"""
    data_tv = urlopen('http://127.0.0.1:8080/getlinktv').read()
    data_tv = json.loads(data_tv.decode('utf-8'))
    titles_tv = []
    for i in range(len(data_tv['linktv'])):
        titles_tv.append('{} - {}'.format(i, data_tv['linktv'][i]['title']))
    return data_tv['linktv'], titles_tv


def loaddatamovie():
    """Calls the function getmovie from server.py and returns a list with all the data about the movies"""
    data_movie = urlopen('http://127.0.0.1:8080/getmovie').read()
    data_movie = json.loads(data_movie.decode('utf-8'))
    titles_movie = []
    for i in range(len(data_movie['linkmovie'])):
        titles_movie.append('{} - {}'.format(i, data_movie['linkmovie'][i]['title']))
    return data_movie['linkmovie'], titles_movie


def loadusers():
    """Calls the function getusers from server.py and returns a list with all the data about the users"""
    data_users = urlopen('http://127.0.0.1:8080/getusers').read()
    data_users = json.loads(data_users.decode('utf-8'))
    users_list = []
    for i in range(len(data_users['users'])):
        users_list.append('{} - {}'.format(i, data_users['users'][i]['username']))
    return data_users['users'], users_list


class AdminAppForm(GridLayout):
    linktv, titles_tv = loaddatatv()
    linktv_spr = ObjectProperty()
    detail_tv_txt = ObjectProperty()
    linkmovie, titles_movie = loaddatamovie()
    linkmovie_spr = ObjectProperty()
    detail_movie_txt = ObjectProperty()
    users, users_list = loadusers()
    user_spr = ObjectProperty()
    detail_users_txt = ObjectProperty()
    i = -1
    j = -1
    k = -1

    def showdetail_tv(self, text):
        """Will show the tv shows loaded in this form """
        if text != '':
            self.i = int(text.split('-')[0].strip())
            tvshow = self.linktv[self.i]
            self.detail_tv_txt.text = '''
            - Title: {}
            - Seasons: {}
            - Votes: {}
            - Year: {}
            - Episodes: {}
            - Genre: {}
            - Actors: {}
            - Description: {}'''.format(tvshow['title'], tvshow['season'], tvshow['votes'], tvshow['year'],
                                        tvshow['episodes'], tvshow['genre'], tvshow['actors'], tvshow['description'])

    def delete_tv(self):
        """will call the function deletelinktv from server.py"""
        data = urlopen('http://127.0.0.1:8080/deletelinktv?i=' + str(self.i))
        data = data.read().decode('utf-8')
        if data == 'OK':

            self.detail_tv_txt.text = ''
            self.linktv_spr.text = ''
            self.linktv, self.linktv_spr.values = loaddatatv()

    def showdetail_movie(self, text):
        """Will show the movies loaded in this form """
        if text != '':
            self.j = int(text.split('-')[0].strip())
            movies = self.linkmovie[self.j]
            self.detail_movie_txt.text = '''
            - Title: {}
            - Year: {}
            - Votes: {}
            - Duration: {}
            - Genre: {}
            - Actors: {}
            - Description: {}'''.format(movies['title'], movies['year'], movies['votes'], movies['time'],
                                        movies['genre'], movies['actors'], movies['description'])

    def delete_movie(self):
        """will call the function deletemovie from server.py"""
        data = urlopen('http://127.0.0.1:8080/deletemovie?i=' + str(self.j))
        data = data.read().decode('utf-8')
        if data == 'OK':
            self.detail_movie_txt.text = ''
            self.linkmovie_spr.text = ''
            self.linkmovie, self.linkmovie_spr.values = loaddatamovie()

    def showdetail_users(self, text):
        """Will show the users loaded in this form """
        if text != '':
            self.k = int(text.split('-')[0].strip())
            users = self.users[self.k]
            self.detail_users_txt.text = '''
            -username: {}
            -email: {}
            -password: {}'''.format(users['username'], users['email'], users['password'])
    
    def delete_users(self):
        """will call the function deleteusers from server.py"""
        data = urlopen('http://127.0.0.1:8080/deleteusers?i=' + str(self.k))
        data = data.read().decode('utf-8')
        if data == 'OK':
            self.detail_users_txt.text = ''
            self.users_spr.text = ''
            self.users, self.user_spr.values = loadusers()


class AdminApp(App):
    title = 'Tvshow & Movies AdminApp'


AdminApp().run()
