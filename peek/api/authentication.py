from rest_framework.authentication import SessionAuthentication


class CSRFExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):  # pragma: no cover
        return   # To not perform the CSRF check previously happening
