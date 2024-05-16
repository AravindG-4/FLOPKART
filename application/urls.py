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
    path('admin_dashboard/add_item/', views.add_item, name="add_item"),
    path('admin_dashboard/update_item/', views.update_item, name="update_item"),
    path('admin_dashboard/remove_item/', views.remove_item, name="remove_item"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)