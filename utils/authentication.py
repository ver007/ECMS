from django.shortcuts import redirect


def auth(func):
    # For user authentication.
    def inner(request, *args, **kwargs):
        if not request.COOKIES.get('is_login'):
            return redirect('/login/')
        return func(request, *args, **kwargs)
    return inner
