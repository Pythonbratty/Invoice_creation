from django.db import models

# Create your models here.
from django.db import models

class Lead(models.Model):
    invoice_number = models.CharField(max_length=100)
    client_name = models.CharField(max_length=300)
    client_email = models.EmailField()
    project_name = models.CharField(max_length=100)
    amount_to_be_charged = models.IntegerField(blank=True, null=True)
