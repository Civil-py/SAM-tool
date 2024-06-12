from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
# from choices import CONTRACT_TYPES, TAX_TYPES, DEDUCTION_TYPES, PAYMENT_TYPES, BANKS_TYPES
# Create your models here.

import datetime
from datetime import timezone

LICENSE_TYPES = [
    ('L', 'Lease'),
    ('W', 'Warranty'),
('M', 'Maintenance')
]

SOFTWARE_TYPES = [
    ('OP', 'On-platform'),
    ('C', 'Cloud')
]

RENEWAL_TYPES = [
    ('RE', 'Renewed'),
    ('NO', 'Not Renewed')
]

DEPARTMENT_TYPES = [
    ('FIN', 'Finance'),
    ('HR', 'Human Resources'),
('IT', 'Technical Support')
]

CATEGORY_TYPES = [
    ('SS', 'System'),
    ('APP', 'Application'),
('MID', 'Middleware'),
('OF', 'Office')
]

Status_TYPES = [
    ('ACT', 'Active'),
    ('PEN', 'Pending'),
    ('DIS', 'In-Active')
]


# Create your models here.
class Staff(models.Model):
    employee_id = models.CharField(max_length=64, primary_key=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64,null=True)
    email = models.EmailField(null=True)
    department = models.CharField(max_length=64, null=True, choices=DEPARTMENT_TYPES)
    position = models.CharField(max_length=64, null=True)

    # utility Fields
    created_date = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = datetime.datetime.today().now()
        self.last_updated = datetime.datetime.today().now()

        super(Staff, self).save(*args, **kwargs)





class Software(models.Model):
    software_id = models.CharField(  max_length=64, primary_key=True)
    software_name = models.CharField(max_length=64)
    status = models.CharField(null=True, choices=Status_TYPES, max_length=64)
    category = models.CharField(null=True, choices=CATEGORY_TYPES, max_length=64)
    contract_value = models.FloatField(null=True, blank=True)
    number_of_licenses = models.FloatField(null=True, blank=True)
    managed_by = models.CharField(null=True, max_length=64)
    software_type = models.CharField(null=True, choices=SOFTWARE_TYPES, max_length=64)
    vendor = models.CharField(max_length=64, null=True)
    number_of_users = models.FloatField(null=True, blank=True, default=0)


    #utility Fields
    created_date = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.software_name}"

    def save(self, *args, **kwargs):
        if self.software_id is None:
            self.software_id = str(uuid4()).split('-')[4]
        if self.created_date is None:
            self.created_date = datetime.datetime.today().now()
        self.last_updated = datetime.datetime.today().now()

        super(Software, self).save(*args, **kwargs)



class Contract(models.Model):
    contract_id = models.CharField(max_length=64, null=True)
    software_id = models.CharField(max_length=64, null=True)
    license_type = models.CharField(max_length=64, null=True, choices=LICENSE_TYPES)
    contact_status = models.CharField(max_length=64, null=True, choices=Status_TYPES)
    renewal_status = models.CharField(max_length=64, null=True, choices=Status_TYPES)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


    # utility Fields
    added = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.software_id} {self.contract_id}"

    def save(self, *args, **kwargs):
        if self.added is None:
            self.added = datetime.datetime.today().now()
        self.last_updated = datetime.datetime.today().now()

        super(Contract, self).save(*args, **kwargs)

class UserAllocation(models.Model):
    assigned = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(Staff, models.CASCADE, blank=True, null=True)
    software = models.ForeignKey(Software, models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"






