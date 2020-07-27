class ReverseProxy(object):
    """
    Reverse proxies can cause some problems within applications, as they change routes, redirect
    traffic, and applications might have errors because of that. This piece of middlewar make sure
    everything runs smoothly.
    """

    def __init__(self, app, script_name=None, scheme=None, server=None, port=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server
        self.port = port

    def __call__(self, environ, start_response):
        """
        This function modifies the environment received by the WSGI, mostly making sure we serve
        the right routes and that the application answers as if it were the initial host (for
        example, an error should say that the site at reverse-proxied.admin.ch/generic_name/generate
        encountered a problem, not that it was at internal.server/generate

        :param environ: the WSGI environment
        :param start_response: A callable accepting headers, a status code and can accept an
        exception to start the response

        :return: a call to the wsgi app, with an updated WSGI environment.
        """
        """
        The first part makes sure the route goes to the right resource.
        If we have a query made to reverse-proxy.admin.ch/generic_name/generate,
        HTTP_X_SCRIPT_NAME will be /generic_name, and PATH_INFO would be /generic_name/generate.

        PATH_INFO is used to handle the route called (in this case, it would use /generate)
        SCRIPT_NAME is used to prefix the routes so that the application returns a correct answer
        (namely: that the query was hitting /generic_name/generate).
        """
        # The syntax here means : try to get HTTP_X_SCRIPT_NAME, or get me an empty string, and the
        # command or, in the context of a string, returns the first "truthy" value
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        # The scheme is the protocol used (http/s) to connect to the server.
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        # this sets our own HOST parameter to be the one that was queried in the first place.
        server = environ.get('HTTP_X_FORWARDED_HOST', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)
