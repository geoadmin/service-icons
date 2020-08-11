from functools import wraps


def prefix_route(route_decorator, prefix='', fmt='{prefix}{route}'):
    '''Defines a new route decorator with a prefix.
    Args:
        route_decorator: route decorator to be enhanced
        prefix: prefix to add to the route
        fmt: string format to use for adding the prefix
    Returns:
        new decorator with prefixed route.
    '''

    @wraps(route_decorator)
    def newroute(route, *args, **kwargs):
        '''New function to prefix the route'''
        return route_decorator(fmt.format(prefix=prefix, route=route), *args, **kwargs)

    return newroute
