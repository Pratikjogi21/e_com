
from django.contrib import admin
from django.urls import path
from Host_Admin.views import *
from UserApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login',admin_login),
    path('admin_logout',logout_view),
    path('home',admin_home),
     path('',registerView,name='registration'),
    path('login',loginView),
    path('homeuser',homeView),
    path('logout',logoutView),
    path('add_product',add_product),
    path('product_list',product_list)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

