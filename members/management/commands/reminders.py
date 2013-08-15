from datetime import date

from django.core.management.base import BaseCommand

from members.models import *


# Run this command once a day to send "expiring soon" and "just expired" warnings to members

def send_expiry_emails(m, date, expiring, expired, internal):
    days = ( date - date.today() ).days
    if days == settings.EXPIRING_DAYS:
        m.send_email(expiring)
    elif days == -1:
        m.send_email(expired)
    elif days == settings.EXPIRING_INTERNAL_DAYS:
        m.send_email(internal, False)

class Command(BaseCommand):
    def handle(self, *args, **kw):
        # this needs to be updated to work for legacy payments
        for m in ( m for m in Member.objects.all()):
            send_expiry_emails(m, m.membership_expiry_date(), "expiring_membership.txt", "expired_memberhip.txt", "internal.txt")
            send_expiry_emails(m, m.access_expiry_date(), "expiring_monthly_access.txt", "expired_monthly_access.txt", "internal.txt")
            send_expiry_emails(m, m.key_expiry_date(), "expiring_key.txt", "expired_key.txt", "internal.txt")

