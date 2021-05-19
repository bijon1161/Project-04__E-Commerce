from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from accounts.models import Guest

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        guest_id = request.session.get('guest_id')
        user = request.user
        obj, created = None, False
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        elif guest_id is not None:
            guest_obj = Guest.objects.get(id=guest_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    # customer_id in stripe or braintree

    def __str__(self):
        return self.email

    objects = BillingProfileManager()


# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print('ACTUAL API REQUEST Send to stripe/braintree')
#         instance.customer_id = new_id
#         instance.save()


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)