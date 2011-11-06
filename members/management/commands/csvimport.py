import datetime, csv, sys

from django.core.management.base import BaseCommand, CommandError
from members.models import *

from datetime import date,datetime
EPOCH=date(2000,1,1)

class Command(BaseCommand):
    args = '<csv-path>'
    help = 'Import members via a CSV from our google docs spreadsheet'

    def handle(self, *args, **kw):
        reader = csv.reader(open(args[0], 'r'), delimiter=',', quotechar='"')
        skip=False
        for fields in reader:
            if not skip: # header
                skip=True
                continue
            try:
                name=fields[3].split(" ")
                first = name[0]
                last = " ".join(name[1:]) # hacky use of >2 name segments                
                try:
                    existing= Member.objects.get(first_name=first, last_name=last)
                    print "Already have a member named %s %s, skipping" % (first, last)
                    continue
                except Member.DoesNotExist:
                    pass

                try:
                    joindate=datetime.strptime(fields[0], "%d/%m/%Y")
                except ValueError:
                    print "Failed to convert date %s" % fields[0]
                    joindate=EPOCH

                member = Member(first_name=name[0], 
                                last_name=" ".join(name[1:]), 
                                join_date=joindate,
                                address=fields[4],
                                emergency_contact_name=fields[8],
                                emergency_contact_number=fields[9],
                                medical_info=fields[10],
                                )
                member.save()
                
                email = Email(member=member, email=fields[6])
                phone = Phone(member=member, phone_number=fields[7])
                email.save()
                phone.save()

            finally:
                pass
            #except BaseException as e:
            #    print "Failed to migrate %s" % (fields,)
            #    print "Error %s" % (e,)
            #    sys.exit(1)

