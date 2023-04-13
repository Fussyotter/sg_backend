from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    productName = models.CharField(max_length=100)
    productCode = models.CharField(max_length=150)
    total = models.IntegerField(
        default=0, null=True, blank=True, verbose_name='Total Count')
    user = models.ManyToManyField(User)
    # completed = models.BooleanField()
    def __str__(self): return self.productName


class Gift(models.Model):
    giftName = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    alternativeLink = models.URLField(max_length=255)

class Supply(models.Model):
    productName = models.CharField(max_length=100)
    productCode = models.CharField(max_length=150)
    stock = models.IntegerField()
    location = models.CharField(max_length=100)
    # This was a fix to my admin view displaying Supplys
    class Meta:
        verbose_name_plural = "Supplies"

    def __str__(self): return self.productName

class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages', null=True)
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages', null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.content

#  useless, tried to use chatgpt to help and got nonsense
# class Conversation(models.Model):
#     user1 = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='conversations1')
#     user2 = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='conversations2')
#     is_seen = models.BooleanField(default=False)


#     def get_other_user(self, current_user):
#         if self.user1 == current_user:
#             return self.user2
#         else:
#             return self.user1
