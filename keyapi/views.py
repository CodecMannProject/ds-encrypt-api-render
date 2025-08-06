from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Key
from .serializers import KeySerializer
from django.http import JsonResponse

class GetKey(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aes_obj = Key.objects.first()
        if aes_obj:
            aes_obj.refresh_if_needed()
            return JsonResponse({
                "key": aes_obj.key,
                "salt": aes_obj.salt
            })
        return JsonResponse({"error": "AES key not found"}, status=404)
