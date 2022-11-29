from django.shortcuts import redirect


class AuthUserMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)