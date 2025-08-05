from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Key
from .serializers import KeySerializer

class GetKey(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        key_obj = Key.objects.get(user=request.user)
        serializer = KeySerializer(key_obj)
        return Response(serializer.data)
