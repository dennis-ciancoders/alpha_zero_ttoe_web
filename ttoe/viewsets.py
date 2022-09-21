# API to get a move from the AI
from ttoe.serializers import TMoveSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

class MoveAPI(generics.CreateAPIView):
    serializer_class = TMoveSerializer
    permission_classes = [AllowAny]