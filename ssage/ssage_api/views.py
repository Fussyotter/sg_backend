from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from .serializers import OrderSerializer, SupplySerializer
from .models import Order, Supply
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


# Create your views here.
class SupplyList(generics.ListCreateAPIView):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self,serializer):
        serializer.save(user=[self.request.user])

class OrdersByUserView(APIView):
    def get(self,request, username):
        orders = Order.objects.filter(user__username=username)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#  chat test functions
def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
