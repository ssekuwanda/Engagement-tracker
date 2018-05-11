from django.contrib import admin
from .models import Client, Payment, Engagement, Proposal, Target,Invoice
from import_export.admin import ImportExportMixin, ExportActionModelAdmin
from import_export.resources import ModelResource

admin.site_header = "Engagement Tracker"

class EngagementResource(ModelResource):
    class Meta:
        model = Engagement

class EngagementAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = EngagementResource
    import_order =('assignment','client','reference','engagement_ending','rate','factor','active','currency','remarks','type')
    list_display =('assignment','client','reference','engagement_ending','rate','factor','active','currency','remarks','type')

class ClientResource(ModelResource):
    class Meta:
        model = Client

class ClientAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ClientResource
    import_order =('name','client_number',)
    list_display =('name','client_number',)


admin.site.register(Client,ClientAdmin)
admin.site.register(Engagement,EngagementAdmin)
admin.site.register(Payment)
admin.site.register(Proposal)
admin.site.register(Target)
admin.site.register(Invoice)
