from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'tracker'

urlpatterns = [
        path('',views.home, name= 'home'),
        path('create-proposal', views.create_proposal, name="create_proposal"),
        path('new-client',views.new_client, name='new_client'),
        path('dashboard', views.dashboard, name='dashboard'),
        path('search',views.search, name='search'),
        path('dashboard/add_target/', views.add_target, name='add_target'),
        path('<int:pk>/detail/', views.detail, name='detail'),
        path('<int:pk>/detail/client-edit', views.ClientEdit.as_view(), name='client_edit'),
        path('<int:pk>/detail/notes/', views.detail, name='notes'),
        path('<int:pk>/create-engagement/', views.create_engagement, name='create_engagement'),
        path('<int:client_id>/detail/<int:engagement_id>/', views.edit_engagement, name='edit_engagement'),
        path('<int:pk>/detail/<int:engagement_pk>/invoices/', views.EngagementInvoice.as_view(), name='engagement_invoices'),
        path('<int:pk>/detail/<int:engagement_pk>/create-invoice/', views.create_invoice, name='create_invoice'),
        path('<int:pk>/detail/<int:engagement_pk>/invoices/<int:invoice_pk>/', views.pay_invoice, name='pay_invoice'),
        re_path(r'^(?P<client_id>[0-9]+)/delete-engagement/^(?P<engagement_id>[0-9]+)/$', views.delete_engagement, name='delete_engagement'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
