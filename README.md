mhvdb is a simple Django app for tracking the state of the [Make, Hack, Void](http://www.makehackvoid.com/)
hackerspace membership & finances. You might find it useful for your Hackerspace or similar organisation, but possibly only if it somewhat resembles MHV in structure.

It is not very complex, and leverages Django admin interface to do most of the heavy lifting.

Features
========

* New version supports expiring and non expiring member products to allow for a range of membership structures. 
	* Examples of expiring member products at MHV are
		* Annual membership
		* Annual membership (concession)
		* Key (6 months)
		* Key (12 months)
		* monthly access (unlimited visits)
	* Examples of non expiring member products at MHV are
		* single visit access
		* book of 10 visits
		
* Provides management of expenses, income & balance sheet predictions, and simple financial reports.

* Provides easy summary page of soon-to-expire or just-expired memberships and other expiring member products.

* Allow a local IP range that can view some common data (membership
  roster, expiries, members' emergency contact info) without logging in
  (see LOCAL_IP_ADDRESSES in settings.py) This is so-far-unused and
  probably not secure.

* Will email members when their membership and other expiring products are about to expire, and/or the Treasurer once membership has expired.

* Provides management of memberships by levels (legacy version), pro rate upgrades & downgrades & membership cost reductions.

* Over 50% Yak Hair Free

Not Features
============

> Things that it would be nice for mhvdb to do, but it doesn't quite do yet

* Full dual entry accounting for income & expenses, or at least better
  management of cash payments & especially cash deposits.

* Management of expense requests/approval, for people claiming money back from the hackerspace

* Integration with payment gateways or bank APIs for automatic data entry.


Requirements
============
To install all required python packages, run `pip install -r requirements.txt`

* [Django 1.5](https://www.djangoproject.com/)

* [South](http://south.aeracode.org/) - For schema management.

* [django-bootstrap-toolkit](https://github.com/dyve/django-bootstrap-toolkit) & [django-admin-bootstrapped](https://github.com/riccardo-forina/django-admin-bootstrapped) - For django + bootstrap integration

Configuration
=============

Create a local_settings.py file for any site-specific additions or changes to settings.py.

There is a comment at the top of settings.py that explains what definitely needs to be in your local_settings.py.


Getting Started
===============

* Set up local_settings.py as described above. "./manage.py syncdb" if necessary to create a database.

* Create an admin account "./manage.py createsuperuser"

* If running with the Django debug server, "./manage.py runserver" and note the site URL.

* Open the site URL, click on 'Admin', and log in with your new admin account

* Create essential data about your organisation (legacy style):
  + "Memberships" are types of membership offered (ie MHV has 'Member' and 'Member (concession) and Expired' membership.)
  + By default, mhvdb assumes you'll add a membership type called "Expired" for any new member, or member whose membership expires. You can override the name of this type in overide_settings.py
  + "Membership Products" are associated with each membership, giving rate for certain period.
  + Products give details 
  
* Create essential data about your organisation (legacy style):
  + "Memberships" are types of membership offered (ie MHV has 'Associate' and 'Full' membership.)
  + By default, mhvdb assumes you'll add a membership type called "Casual" for any new member, or member whose membership expires. You can override the name of this type in overide_settings.py
  + "Membership Costs" are associated with each membership, giving a per-month rate. Costs can change over time, each cost has a "valid from" field which determines when it applies from. If a membership's costs go down over time, mhvdb will automatically grant a pro rata extension of membership to current members already paid (the converse does not apply, if membership costs go up there is no pro rata shortening!)

* Add specific data from your organisation:
  + "Member" is self-explanatory, basic personal data about members.
  + Each Member has one or more "Member Payments" and "Expiring Member Payments", which are the payments they make to become members.

  + Expenses & Income are for one-off costs or income the organisation incurs.

  + RecurringExpenses are for costs that repeat reliably over a period of time.


FAQ
===

* How do I add a membership renewal (legacy version)?
  + View the member's entry under Admin -> Members, and there is a list of Member Payments at the bottom.
    Add a new one for the member, making sure the "Continues Membership" box is checked if this is a renewal.

* What happens if a member upgrades/downgrades their membership type before it expires (legacy version)?
  +  Supported! Add a new Member Payment (it can be $0 if they're not paying anything at that time), with the
     new membership type and check "Existing Member Changing Type". Their membership will be
     recalculated as the new type, reusing any left over membership they had from the old type.


Contributors
============

- Angus Gratton
- Brenda Moon
- Cameron Moon
- Geoff Swan
- Tim Suess

... further contributors very welcome. :)

