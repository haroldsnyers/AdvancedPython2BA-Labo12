import json
import os

import cherrypy
from cherrypy.lib.static import serve_file
import jinja2

import jinja2plugin
import jinja2tool


class WebApp:
    """Web application of the Tv shows and Movies application"""
    def __init__(self):
        self.linktv = self.loadlinktv()
        self.linkmovie = self.loadmovies()
        self.users = self.loadusers()

    def loadusers(self):
        """Loads users' database from the 'users.json' file."""
        try:
            with open('users.json', 'r') as file:
                content = json.loads(file.read())
                return content['users']
        except:
            cherrypy.log('Loading database failed.')
            return []

    def saveusers(self):
        """Saves users' database to the 'users.json' file."""
        try:
            with open('users.json', 'w') as file:
                file.write(json.dumps({
                    'users': self.users
                }, ensure_ascii=False, indent=3))
        except:
            cherrypy.log('Saving database failed.')

    def savelinkstv(self):
        """Saves tv shows' database to the 'db.json' file."""
        try:
            with open('db.json', 'w') as file:
                file.write(json.dumps({
                    'linktv': self.linktv
                }, ensure_ascii=False, indent=3))
        except:
            cherrypy.log('Saving database failed.')

    def loadlinktv(self):
        """Loads tv shows' database from the 'db.json' file."""
        try:
            with open('db.json', 'r') as file:
                content = json.loads(file.read())
                return content['linktv']
        except:
            cherrypy.log('Loading database failed.')
            return []

    def savemovies(self):
        """Saves movies' database to the 'movie.json' file."""
        try:
            with open('movie.json', 'w') as file:
                file.write(json.dumps({
                    'linkmovie': self.linkmovie
                }, ensure_ascii=False))
        except:
            cherrypy.log('Saving database failed.')

    def loadmovies(self):
        """Loads the movies' database from the 'movie.json' file."""
        try:
            with open('movie.json', 'r') as file:
                content = json.loads(file.read())
                return content['linkmovie']
        except:
            cherrypy.log('Loading database failed.')
            return []

    def user_session(self):
        """It determines if you are logged in or out, and displays the buttons according to this."""
        user_session = ''
        if cherrypy.session.get('user') is None:
            user_session = ''' <li><a href="index">Home</a></li>'''

        if cherrypy.session.get('user') is not None:
            user_session = '''<li><a href="tvshows">Tv Shows</a></li>
                      <li><a href="movies">Movies</a></li>'''
        return user_session

    @cherrypy.expose
    def index(self):
        """homepage of the website."""
        usersession = ''
        if cherrypy.session.get('user') is None:
            usersession = '''<input id="button" type="button" name="answer" value="Login" onclick="showDiv()" />'''

        if cherrypy.session.get('user') is not None:
            usersession = '''<p id="button">{}/<a href="logout">logout</a></p>'''.format(cherrypy.session.get('user'))

        return {'user': self.user_session(), 'usersession': usersession}

    @cherrypy.expose
    def tvshows(self):
        """page which includes all the tvshows that have been added"""
        usersession = ''
        if cherrypy.session.get('user') is None:
            usersession = '''<input id="button" type="button" name="answer" value="Login" onclick="showDiv()" />'''

        if cherrypy.session.get('user') is not None:
            usersession = '''<p id="button">{}/<a href="logout">logout</a></p>'''.format(cherrypy.session.get('user'))
            if len(self.linktv) == 0:
                linktv = '<p>No Tv Shows in the database.</p>'
            else:
                self.linktv.sort(key=lambda k: k['votes'], reverse=True)
                linktv = ''
                for i in range(len(self.linktv)):
                    tv = self.linktv[i]
                    linktv += '''
                    <tr><td><strong>{}</strong></td><td>{}</td><td id="hoverD"><ul><li><h3>Year:</h3>{}</li><li>
                    <h3>Number of Episodes:</h3>{}</li><li><h3>Genre:</h3>{}</li><li><h3>Summary:</h3> <small>{}</small>
                    </li><li><h3>Actors:</h3>{}</li></ul></td><td>{}</td><td><a href="addvotetv?i={}">+1</a></td>
                    </tr>'''.format(tv['title'], tv['season'], tv['year'], tv['episodes'], tv['genre'],
                                    tv['description'], tv['actors'], tv['votes'], i)

        return {'linktv': linktv, 'user': self.user_session(), 'usersession': usersession}

    @cherrypy.expose
    def movies(self):
        """page which includes all the movies that have been added"""
        usersession = ''
        if cherrypy.session.get('user') is None:
            usersession = '''<input id="button" type="button" name="answer" value="Login" onclick="showDiv()" />'''

        if cherrypy.session.get('user') is not None:
            usersession = '''<p id="button">{}/<a href="logout">logout</a></p>'''.format(cherrypy.session.get('user'))
            if len(self.linkmovie) == 0:
                linkmovie = '<p>No Tv Shows in the database.</p>'
            else:
                self.linkmovie.sort(key=lambda k: k['votes'], reverse=True)
                linkmovie = ''
                for i in range(len(self.linkmovie)):
                    movie = self.linkmovie[i]
                    linkmovie += '''
                    <tr><td><strong>{}</strong></td><td id="hoverD"><ul><li><h3>Year:</h3>{}</li><li><h3>Duration:
                    </h3>{} minutes</li><li><h3>Genre:</h3>{}</li><li><h3>Summary:</h3> <small>{}</small></li><li>
                    <h3>Actors:</h3>{}</li></ul></td><td>{}</td><td><a href="addvotemovie?i={}">+1</a></td>
                    </tr>'''.format(movie['title'],  movie['year'], movie['time'], movie['genre'], movie['description'],
                                    movie['actors'], movie['votes'], i)

        return {'linkmovie': linkmovie, 'user': self.user_session(), 'usersession': usersession}

    @cherrypy.expose
    def addtvmovie(self):
        """Page with 2 forms to add new movies or tv shows"""
        if cherrypy.session.get('user') is not None:
            return {'user': self.user_session()}

        else:
            raise cherrypy.HTTPRedirect('/logincall')

    @cherrypy.expose
    def about(self):
        """page with news about the web designers, the website and further information"""
        usersession = ''

        if cherrypy.session.get('user') is None:
            usersession = '''<input id="button" type="button" name="answer" value="Login" onclick="showDiv()" />'''

        if cherrypy.session.get('user') is not None:
            usersession = '''<p id="button">{}/<a href="logout">logout</a></p>'''.format(cherrypy.session.get('user'))

        return {'user': self.user_session(), 'usersession': usersession}

    @cherrypy.expose
    def register(self):
        """page to register into the website"""
        return {'user': self.user_session()}

    @cherrypy.expose
    def createusers(self, uname, email, psw):
        """POSt route to add a new user to the database."""
        if len(self.users) == 0:
            cherrypy.session['user'] = uname
            self.users.append({
                'username': uname,
                'email': email,
                'password': psw,
            })
            self.saveusers()
            raise cherrypy.HTTPRedirect('/')

        for i in range(len(self.users)):
            usersdb = self.users[i]
            if uname == usersdb['username']:
                user_error = '<h2 class="error">Username already taken!</h2>'

                return {'user_error': user_error}

        for i in range(len(self.users)):
            usersdb = self.users[i]
            if email == usersdb['email']:
                email_error = '<h2 class="error">Email already in use!</h2>'

                return {'email_error': email_error}

        cherrypy.session['user'] = uname
        self.users.append({
            'username': uname,
            'email': email,
            'password': psw,
        })
        self.saveusers()
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def login(self, uname, psw):
        """function to login into the website"""
        print(str(self.users))
        for i in range(len(self.users)):
            usersdb = self.users[i]
            print(str(usersdb))
            if uname == usersdb['username'] and psw == usersdb['password']:
                cherrypy.session['user'] = uname
                raise cherrypy.HTTPRedirect('tvshows')

        login_error = '<h2 class="error">Wrong username or password!</h2>'
        return {'login_error': login_error, 'user': self.user_session()}

    @cherrypy.expose
    def logout(self):
        """function to logout of your session"""
        del(cherrypy.session['user'])
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def logincall(self):
        """Page with a form to login."""
        return {'user': self.user_session()}

    @cherrypy.expose
    def addlinktv(self, title, seasons, year, episodes, genre, actors, description):
        """POST route to add a new tv show to the database."""
        if title != '' and seasons != '':
            self.linktv.append({
                'title': title,
                'season': seasons,
                'year': year,
                'episodes': episodes,
                'genre': genre,
                'actors': actors,
                'description': description,
                'votes': 1
            })
            self.savelinkstv()
        raise cherrypy.HTTPRedirect('tvshows')

    @cherrypy.expose
    def addvotetv(self, i):
        """GET route to add one vote for a given tv show."""
        try:
            self.linktv[int(i)]['votes'] += 1
            self.savelinkstv()
        except:
            pass
        raise cherrypy.HTTPRedirect('tvshows')

    @cherrypy.expose
    def getlinktv(self):
        """GET route to get all the tv shows."""
        return json.dumps({
            'linktv': self.linktv
        }, ensure_ascii=False).encode('utf-8')

    @cherrypy.expose
    def deletelinktv(self, i):
        """GET route to delete a tv show."""
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.linktv):
            del (self.linktv[i])
            result = 'OK'
            self.savelinkstv()
        return result.encode('utf-8')

    @cherrypy.expose
    def addmovie(self, title, year, time, genre, description, actors):
        """POST route to add a new movie to the database."""
        if title != '':
            self.linkmovie.append({
                'title': title,
                'year': year,
                'time': time,
                'genre': genre,
                'description': description,
                'actors': actors,
                'votes': 1
            })
            self.savemovies()
        raise cherrypy.HTTPRedirect('movies')

    @cherrypy.expose
    def addvotemovie(self, i):
        """GET route to add one vote for a given movie."""
        try:
            self.linkmovie[int(i)]['votes'] += 1
            self.savemovies()
        except:
            pass
        raise cherrypy.HTTPRedirect('movies')

    @cherrypy.expose
    def getmovie(self):
        """GET route to get all the movies."""
        return json.dumps({
            'linkmovie': self.linkmovie
        }, ensure_ascii=False).encode('utf-8')

    @cherrypy.expose
    def deletemovie(self, i):
        """GET route to delete a movie."""
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.linkmovie):
            del (self.linkmovie[i])
            result = 'OK'
            self.savemovies()
        return result.encode('utf-8')

    @cherrypy.expose
    def getusers(self):
        """GET route to get all the users"""
        return json.dumps({
            'users': self.users
        }, ensure_ascii=False).encode('utf-8')

    @cherrypy.expose
    def deleteusers(self, i):
        """GET route to delete an user."""
        result = 'KO'
        i = int(i)
        if 0 <= i < len(self.users):
            del (self.users[i])
            result = 'OK'
            self.saveusers()
        return result.encode('utf-8')


if __name__ == '__main__':
    # Register Jinja2 plugin and tool
    ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
    jinja2plugin.Jinja2TemplatePlugin(cherrypy.engine, env=ENV).subscribe()
    cherrypy.tools.template = jinja2tool.Jinja2Tool()

    # Launch web server
    CURDIR = os.path.dirname(os.path.abspath(__file__))
    cherrypy.quickstart(WebApp(), '', "server.conf")
