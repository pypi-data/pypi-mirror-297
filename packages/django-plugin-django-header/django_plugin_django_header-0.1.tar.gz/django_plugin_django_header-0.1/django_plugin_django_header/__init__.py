import djp


@djp.hookimpl
def middleware():
    return ["django_plugin_django_header.middleware.DjangoHeaderMiddleware"]
