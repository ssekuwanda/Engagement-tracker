from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'tracker'

urlpatterns = [
        path('',views.home, name= 'home'),
        path('new-client',views.new_client, name='new_client'),
        path('new-proposal',views.new_proposal, name='new_proposal'),
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
        path('<int:pk>/detail/<int:engagement_pk>/invoices/<int:pay_pk>/pay/', views.create_payment, name='create_payment'),
        re_path(r'^(?P<client_id>[0-9]+)/delete-engagement/^(?P<engagement_id>[0-9]+)/$', views.delete_engagement, name='delete_engagement'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
