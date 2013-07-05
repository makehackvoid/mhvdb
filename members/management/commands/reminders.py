from datetime import date

from django.core.management.base import BaseCommand

from members.models import *


# Run this command once a day to send "expiring soon" and "just expired" warnings to members

class Command(BaseCommand):
    def handle(self, *args, **kw):
        for m in ( m for m in Member.objects.all() if m.memberpayment_set.count() > 0 ):
            days = ( m.expiry_date() - date.today() ).days
            if days == settings.EXPIRING_DAYS:
                m.send_email("expiring.txt")
            elif days == -1:
                m.send_email("expired.txt")
            elif days == settings.EXPIRING_INTERNAL_DAYS:
                m.send_email("internal.txt", False)

