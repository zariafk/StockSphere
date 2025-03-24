from django.urls import path
from . import views

urlpatterns = [
    # AUTHENTICATION endpoints
    path('api/set-csrf-token', views.set_csrf_token, name='set_csrf_token'),
    path('api/login', views.login_view, name='login'),
    path('api/logout', views.logout_view, name='logout'),
    path('api/user', views.user, name='user'),
    path('api/register', views.register, name='register'),

    #RESOURCES endpoints
    path('api/resources', views.get_resources, name='get_resources'),
    path('api/resources/add', views.add_resource, name='add_resource'),
    path('api/resources/<int:resource_id>/update', views.update_resource, name='update_resource'),
    path('api/resources/<int:resource_id>/delete', views.delete_resource, name='delete_resource'),
]
