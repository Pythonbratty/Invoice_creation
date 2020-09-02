from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('invoice_number', 'client_name', 'client_email', 'project_name','amount_to_be_charged')
