from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from .sse import SSEManager
from django.db.models import Model

# You can update the signals like so for different bindings

# @receiver(post_save, sender=HighScore)
# def high_score_update_signal(sender, instance, **kwargs):
#     if instance.is_highest:
#         # Notify all listeners about the new high score and the user
#         SSEManager.notify_listeners(sender.__name__, instance.pk, 'score', instance.score)
#         SSEManager.notify_listeners(sender.__name__, instance.pk, 'user', instance.user.username)

@receiver(post_save)
def model_update_signal(sender, instance, **kwargs):

    for field in instance._meta.fields:
        field_name = field.name
        new_value = getattr(instance, field_name, None)

        if new_value is not None:
            SSEManager.notify_listeners(sender.__name__, instance.pk, field_name, new_value)


def setup_signals(app_label, model_name, signal_handler):
    model = apps.get_model(app_label, model_name)
    post_save.connect(signal_handler, sender=model)