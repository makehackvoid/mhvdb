import datetime, csv, sys

from django.core.management.base import BaseCommand, CommandError
from members.models import *

EPOCH=datetime.datetime.strptime("1/1/2000", "%d/%m/%Y")

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
                member = Member(first_name=name[0], 
                                last_name=" ".join(name[1:]), 
                                join_date=EPOCH,
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


                memtype=fields[11].replace(" Member", "").replace("Student", "Concession")
                memtype=Membership.objects.get(membership_name=memtype)
                
                paytype= fields[13] if len(fields) > 13 else "Bank"
                if "free" in paytype:
                    continue # only George, not worth automating
                if paytype == "" or paytype.startswith("Bank"):
                    paytype = 'Bank Transfer'
                else:
                    paytype = 'Cash'
                
                print fields
                duration={
                    "Six Months" : 6,
                    "Three Months" : 3,
                    "One Month" : 1 }.get(fields[12] if len(fields)>12 else "", "0")

                try:
                    joindate=datetime.datetime.strptime(fields[0], "%d/%m/%Y")
                except ValueError:
                    joindate=EPOCH

                dummypayment=MemberPayment(member=member,
                                           membership_type=memtype,
                                           payment_type=paytype,
                                           payment_value=-1,
                                           date=joindate,
                                           duration=duration,
                                           continues_membership=False)
                dummypayment.save()
                

            finally:
                pass
            #except BaseException as e:
            #    print "Failed to migrate %s" % (fields,)
            #    print "Error %s" % (e,)
            #    sys.exit(1)

