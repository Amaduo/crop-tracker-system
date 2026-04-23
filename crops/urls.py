from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fields/', views.fields_view, name='fields'),
    path('create/', views.create_field, name='create_field'),
    path('update/<int:id>/', views.update_field, name='update'),
    path('updates/', views.view_updates, name='updates'),
    path('updates_page/', views.updates_page, name='updates_page'),
    path('agent_dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent_base/', views.agent_base, name='agent_base'),
    path('field_updates/<int:id>/', views.field_updates, name='field_updates'),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agent_dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('updates_page/<int:id>/', views.field_updates, name='updates_page')
]