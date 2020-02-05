import logging

import simplejson as json
import tornado.gen
from tornado_cors import CorsMixin
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web
import torngithub
from tornado.httputil import url_concat
from torngithub import json_decode, json_encode

log = logging.getLogger("github.demo")


class BaseHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = 'https://gdashboard.netlify.com'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)


# These three routes are not needed since org and token are in the environment
class GithubLoginHandler(CorsMixin, tornado.web.RequestHandler, torngithub.GithubMixin):
    CORS_ORIGIN = 'https://gdashboard.netlify.com'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600
    @tornado.gen.coroutine
    def get(self):
        # we can append next to the redirect uri, so the user gets the
        # correct URL on login
        redirect_uri = url_concat(self.request.protocol
                                  + "://" + self.request.host
                                  + self.settings["github_callback_path"],
                                  {"next": self.get_argument('next', '/')})

        # if we have a code, we have been authorized so we can log in
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=self.settings["github_client_id"],
                client_secret=self.settings["github_client_secret"],
                code=self.get_argument("code"))
            if user:
                log.info('logged in user from github: ' + str(user))
                self.set_secure_cookie("user", json_encode(user))
            else:
                self.clear_cookie("user")
            self.redirect("/token")
            return

        # otherwise we need to request an authorization code
        yield self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.settings["github_client_id"],
            extra_params={"scope": self.settings['github_scope'], "foo": 1})


class GetToken(BaseHandler, torngithub.GithubMixin):
    CORS_ORIGIN = 'https://gdashboard.netlify.com'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # print(self.get_auth_client())
        # self.write(json.dumps({'token': self.current_user['access_token']}))
        self.write(json.dumps({"user_details": {
                    "avatar_url": self.current_user["avatar_url"],
                    "name": self.current_user["name"],
                    "email": self.current_user['email'],
                    "login": self.current_user['login'],
                    "id": self.current_user['id'],
                    "access_token": self.current_user['access_token']
                    },}))


class LogoutHandler(BaseHandler):
    CORS_ORIGIN = 'https://gdashboard.netlify.com'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

