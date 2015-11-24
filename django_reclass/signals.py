from django.dispatch import Signal

push_to_master = Signal(providing_args=["template"])
