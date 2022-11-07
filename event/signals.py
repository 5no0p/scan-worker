from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from .tasks import adding
from .models import Event


@receiver(post_save, sender=Event)
def room_save_handler(sender, created, instance, **kwargs):
    adding.delay(1,2)
    status = 'CREATE' if created else 'UPDATE'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "event",
        {
            'type': 'scaned_ticket',
            'status': status,
            'data': { 
                'id': str(instance.id),
                'name': instance.name
            },
        }
    )