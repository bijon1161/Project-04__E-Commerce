from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from accounts.signals import user_logged_in
from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL
FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_END_SESSION = getattr(settings, 'FORCE_INACTIVE_END_SESSION', False)



class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null=True)
    ip_address      = models.CharField(max_length=100, blank=True, null=True)
    content_type    = models.ForeignKey(ContentType, on_delete=models.CASCADE)    # User, Product, Order, Cart, Address
    object_id       = models.PositiveIntegerField()     # User.id, Product.id, Order.id, Cart.id, Address.id
    content_object  = GenericForeignKey('content_type', 'object_id')    # User/Product/Order/Cart/Address instance
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed at %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']   # most recent show first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)    # instance.__class__
    new_obj_vw = ObjectViewed.objects.create(
        user=request.user,
        ip_address=get_client_ip(request),
        content_type=content_type,
        object_id=instance.id
    )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active     = models.BooleanField(default=True)
    ended     = models.BooleanField(default=False)

    def end_session(self):
        ended = self.ended
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended


def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for q in qs:
            q.end_session()

    if not instance.active and not instance.ended:
        instance.end_session()


if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)


def post_save_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for q in qs:
                q.end_session()


if FORCE_INACTIVE_END_SESSION:
    post_save.connect(post_save_changed_receiver, sender=UserSession)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key

    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)