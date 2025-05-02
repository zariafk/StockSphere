from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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

    #PRODUCTS endpoints
    path('api/products', views.get_products, name='get_products'),
    path('api/products/add', views.add_product, name='add_product'),
    path('api/products/<int:product_id>/update', views.update_product, name='update_product'),
    path('api/products/<int:product_id>/delete', views.delete_product, name='delete_product'),

    #DELIVERIES endpoints
    path('api/deliveries', views.get_deliveries, name='get_deliveries'),
    path('api/deliveries/add', views.add_delivery, name='add_delivery'),
    path('api/deliveries/<int:delivery_id>/update', views.update_delivery, name='update_delivery'),
    path('api/deliveries/<int:delivery_id>/delete', views.delete_delivery, name='delete_delivery'),

    #2FA
    path('api/verify-2fa', views.verify_2fa_view),

    #FORGOT PASSWORD
    path('password_reset', views.password_reset_request, name='password_reset_request'),
    path('password_reset_done', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete', views.password_reset_complete, name='password_reset_complete'),

    #NNOTIFICATIONS
    path('api/dashboard', views.dashboard, name='dashboard'),
]
