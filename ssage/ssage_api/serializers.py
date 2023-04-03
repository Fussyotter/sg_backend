from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, Supply


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = [str(user) for user in instance.user.all()]
        return rep


class SupplySerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Supply
            fields = '__all__'
            pluralize = False
