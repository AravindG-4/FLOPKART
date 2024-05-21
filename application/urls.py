from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_dashboard/user_management/', views.user_management, name="user_management"),
    path('admin_dashboard/user_management/delete_user/', views.delete_user, name="delete_user"),
    path('admin_dashboard/user_management/seller_details/', views.seller_details, name="seller_details"),
    path('admin_dashboard/admin_analytics/', views.admin_analytics, name="admin_analytics"),
    path('admin_dashboard/product_management/', views.product_management, name="product_management"),
    path('admin_dashboard/product_management/add_product/', views.add_product, name="add_product"),
    path('admin_dashboard/product_management/update_product/', views.update_product, name="update_product"),
    path('admin_dashboard/orderlogs/', views.orderlogs, name="orderlogs"),
    path('admin_dashboard/orderform/', views.orderform, name="orderform"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)