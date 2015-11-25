from django.dispatch import receiver
from .signals import push_to_master


@receiver(push_to_master)
def push_to_master(sender, template=None, **kwargs):
    """If Reclass Template sync = True push to master
    """

    #if template and template.sync is True:
    #    template.push()
    pass
