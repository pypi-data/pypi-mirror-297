from django.utils.translation import gettext_lazy as _

from utilities.choices import ChoiceSet


__all__ = (
    'VoiceDeliveryStatusChoices',
    'SopBoolChoices',
    'VoiceMaintainerStatusChoice',
)


class VoiceMaintainerStatusChoice(ChoiceSet):

    CHOICES = (
        ('active', _('Active'), 'green'),
        ('retired', _('Retired'), 'red'),
        ('unknown', _('Unknown'), 'gray'),
    )


class VoiceDeliveryStatusChoices(ChoiceSet):

    CHOICES = (
        ('active', _('Active'), 'green'),
        ('planned', _('Planned'), 'cyan'),
        ('staging', _('Staging'), 'blue'),
        ('retired', _('Retired'), 'red'),
        ('unknown', _('Unknown'), 'gray'),
    )


class SopBoolChoices(ChoiceSet):

    CHOICES = (
        ('unknown', _('Unknown'), 'gray'),
        ('true', _('True'), 'green'),
        ('false', _('False'), 'red'),
    )
