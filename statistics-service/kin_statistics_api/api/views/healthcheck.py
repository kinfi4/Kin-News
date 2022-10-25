from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class HealthCheckView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        from django.contrib.auth.models import User
        print(User.objects.all())
        return Response(data={'status': 'OK'})
