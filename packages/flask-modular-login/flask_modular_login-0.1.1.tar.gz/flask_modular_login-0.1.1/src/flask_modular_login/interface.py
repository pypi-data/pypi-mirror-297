import json, os.path, functools
import flask, flask_caching

import sys, os.path; end_locals, start_locals = lambda: sys.path.pop(0), (
    lambda x: x() or x)(lambda: sys.path.insert(0, os.path.dirname(__file__)))

from store import FKDatabase, FKHeadless
from utils import RouteLobby, relpath, project_path
from tokens import DBStore, methods, authorized, safe_redirect
from access import AccessRoot

end_locals()

oauth_lobby = RouteLobby()

class OAuthBlueprint(flask.Blueprint):
    _oauth_name = "modular_login"
    _credentials_paths = ((), ("run",))
    _oauth_run_path = ("run",)
    # primarily for the sake of access group HTTP api endpoints
    _version = None

    def __init__(
            self, name=None, import_name=None, static_folder=None,
            static_url_path=None, template_folder=None, url_prefix=None,
            subdomain=None, url_defaults=None, root_path=None, cli_group=None):
        name = self._oauth_name if name is None else name
        import_name = __name__ if import_name is None else import_name
        root_path = project_path() if root_path is None else root_path
        url_prefix = "/login" if url_prefix is None else url_prefix
        if self._version is not None:
            url_prefix += "/" + self._version
        super().__init__(
            name, import_name, static_folder, static_url_path, template_folder,
            url_prefix, subdomain, url_defaults, root_path, cli_group)

        self._oauth_root_path = root_path
        self._oauth_run_root = os.path.join(root_path, *self._oauth_run_path)
        self._oauth_apps = []
        self._get_oauth_keys()
        oauth_lobby.register_lobby(self, self)
        self.record(lambda setup_state: self._oauth_register(setup_state.app))

        self.group = AccessRoot(self._oauth_db, OAuthBlueprint.login_endpoint)
        self.register_blueprint(self.group.bp)

    def _get_oauth_keys(self):
        for rel in self._credentials_paths:
            path = os.path.join(self._oauth_run_root, *rel, "credentials.json")
            if os.path.exists(path):
                with open(path) as f:
                    self._oauth_keys = json.load(f)
                return
        self._oauth_keys = {
            name: {"id": "", "secret": ""} for name in methods.keys()}

    @oauth_lobby.route("/")
    def login_base_route(self):
        url = flask.request.args.get("next")
        if url is not None and not safe_redirect(url):
            flask.abort(400)
        if not authorized(): # only accessed in auth app's context
            url = {} if url is None else {"next": url}
            debug = all(i.debug for i in self._oauth_apps)
            # method.login is a flask-dance interface
            return flask.render_template("login.html", debug=debug, **{
                name: flask.url_for(method.name + ".login", **url)
                for name, method in self._oauth_blueprints.items()})
        # TODO: allow custom fallback endpoint
        return flask.redirect("/" if url is None else url)

    def _oauth_deauthorize(self, token, method, callback=None):
        self._oauth_stores[method].deauthorize(token, callback=callback)

    def _oauth_db(self, app=None):
        app = app or flask.current_app
        db_path = os.path.join(self._oauth_run_root, "users.db")
        if app:
            return FKDatabase(
                app, db_path, relpath("schema.sql"), debug=app.debug)
        else:
            return FKHeadless(db_path, relpath("schema.sql"))

    def _oauth_register(self, app):
        self._oauth_apps.append(app)
        db = self._oauth_db(app)
        cache = flask_caching.Cache(app, config={
            'CACHE_MEMCACHED_SERVERS': [project_path("run", "memcached.sock")],
            'CACHE_TYPE': 'utils.threaded_client'})
        stores, blueprints = {}, {}
        # keep version out of redirect since that's provider facing
        for name, (_, factory, scope) in methods.items():
            stores[name] = DBStore(
                db, name, cache, lambda: self.session(app),
                *app.config.get("TIMEOUTS", ()))
            blueprints[name] = factory(
                client_id=self._oauth_keys[name]["id"],
                client_secret=self._oauth_keys[name]["secret"],
                redirect_url=f"/login/{name}/continue",
                storage=stores[name],
                scope=scope
            )
            app.register_blueprint(
                url_prefix=self.url_prefix, blueprint=blueprints[name])

        self._oauth_blueprints = blueprints
        self._oauth_stores = stores

    @staticmethod
    def login_endpoint(app=None):
        app = app or flask.current_app
        # TODO: why isn't this just a url_for call?
        return next(
            i.rule for i in app.url_map.iter_rules()
            if i.endpoint == f"{OAuthBlueprint._oauth_name}.login_base_route")

    @staticmethod
    def session(app):
        if flask.current_app == app and not isinstance(
                flask.session, flask.sessions.NullSession):
            return flask.session
        return app.session_interface.open_session(app, flask.request)

