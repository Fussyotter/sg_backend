from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from  django.views.decorators.csrf import csrf_exempt

from .serializers import OrderSerializer, SupplySerializer, MessageSerializer
from .models import Order, Supply, Message
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class SupplyList(generics.ListCreateAPIView):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self,serializer):
        serializer.save(user=[self.request.user])


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# @login_required
class OrdersByUserView(APIView):
    def get(self,request, username):
        orders = Order.objects.filter(user__username=username)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#  chat test functions

#  THIS ONE WORKS, TESTING NEW ONE ON LINE 46

# class ChatView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, room_name=None):
#         if room_name:
#             return render(request, "chat/room.html", {"room_name": room_name})
#         else:
#             return render(request, "chat/index.html")


class ChatView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, recipient_username):
        recipient = self.get_user(recipient_username)
        content = request.data.get('content')
        if not content:
            return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(
            sender=request.user, recipient=recipient, content=content, timestamp=timezone.now())
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_messages(self, recipient_username):
        sender = self.request.user
        recipient = self.get_user(recipient_username)
        messages = Message.objects.filter(
            (Q(sender=sender) & Q(recipient=recipient)) | (
                Q(sender=recipient) & Q(recipient=sender))
        ).order_by('timestamp')
        return messages

    def get(self, request, recipient_username):
        messages = self.get_messages(recipient_username)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def delete(self, request, recipient_username, message_id):
        message = Message.objects.get(pk=message_id)
        if message.sender != request.user:
            return Response({'error': 'You are not authorized to delete this message.'}, status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CONSUMER REAL TIME TEST NUMBER 1290312U81239012839012839
# 

@csrf_exempt
def send_message(request, recipient_username):
    if request.method == 'POST':
        recipient = User.objects.get(username=recipient_username)
        content = request.POST.get('content')
        if not content:
            return HttpResponseBadRequest('Message content is required.')

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content,
            timestamp=timezone.now()
        )

        # Send message to chat consumer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % recipient_username,
            {
                'type': 'chat_message',
                'message': message.content
            }
        )

        return JsonResponse(MessageSerializer(message).data)
