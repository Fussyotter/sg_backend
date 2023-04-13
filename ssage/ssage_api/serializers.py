from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, Supply, Message, Gift


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = [str(user) for user in instance.user.all()]
        return rep


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'

class SupplySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Supply
            fields = '__all__'
            pluralize = False


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    recipient = serializers.CharField()

    class Meta:
        model = Message
        fields = ['id', 'sender_username',
                  'recipient', 'content', 'timestamp','is_seen']

    def create(self, validated_data):
        recipient_username = validated_data.pop('recipient_username')
        recipient = User.objects.get(username=recipient_username)
        message = Message.objects.create(recipient=recipient, **validated_data)
        return message
#   TESTING CONVERSATION SERIALIZER


# class ConversationSerializer(serializers.ModelSerializer):
#     other_user = serializers.SerializerMethodField()

#     class Meta:
#         model = Conversation
#         fields = ('id', 'other_user', 'is_seen')

#     def get_other_user(self, obj):
#         request_user = self.context['request'].user
#         if obj.user1 == request_user:
#             return obj.user2.username
#         else:
#             return obj.user1.username
class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['is_seen']
