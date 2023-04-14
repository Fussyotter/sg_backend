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

from .serializers import OrderSerializer, SupplySerializer, MessageSerializer, MessageUpdateSerializer, GiftSerializer
from .models import Order, Supply, Message, Gift
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


class GiftList(generics.ListCreateAPIView):
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer

    def perform_create(self, serializer):
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
    # get_messages

    def get_messages(self):
        user = self.request.user
        messages = Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('timestamp')
        return messages

    def get(self, request, recipient_username):
        messages = self.get_messages()
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
#  trying to create a way to view inbox for display on frontend
class InboxView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = request.user
        conversations = []

        # Retrieve all the users who have had conversations with the current user
        participants = Message.objects.filter(Q(sender=user) | Q(
            recipient=user)).values_list('sender', 'recipient').distinct()

        # For each conversation, get the latest message and serialize it
        for participant in participants:
            other_user_id = participant[0] if participant[0] != user.id else participant[1]
            other_user = User.objects.get(id=other_user_id)
            latest_message = Message.objects.filter(Q(sender=user, recipient=other_user) | Q(
                sender=other_user, recipient=user)).latest('timestamp')
            conversations.append({
                'other_user': other_user.username,
                'latest_message': MessageSerializer(latest_message).data
            })

        return Response(conversations)

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
#  trying to do a patch request for updating the is_seen value. couldn't bundle it in because it's for a specific message at a time
class MessageUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        message_id = self.kwargs['message_id']
        try:
            message = Message.objects.get(id=message_id)
            if message.sender != self.request.user and message.recipient != self.request.user:
                raise Http404('no way jose')
            return message
        except Message.DoesNotExist:
            raise Http404

    def patch(self, request, *args, **kwargs):
        message = self.get_object()
        serializer = self.get_serializer(
            message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class MessageDeleteView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        message_id = self.kwargs['message_id']
        try:
            message = Message.objects.get(id=message_id)
            if message.sender != self.request.user:
                raise PermissionDenied(
                    'You are not authorized to delete this message.')
            return message
        except Message.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
