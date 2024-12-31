
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
    path('product_list',product_list),
    path('admin_product_list',admin_product_list),
    path('delete_product/<int:product_id>',delete_product),
    path('update_product/<int:product_id>',update_product),
    path('view_orders',vieworders),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
     path('order/<int:product_id>/',create_order, name='create_order'),
    
    path('add-to-cart/<int:product_id>',add_to_cart),
    # path('remove-to-cart/<int:product_id>',remove_from_cart),
    path('cart',cart_detail),
    path('order/<int:order_id>/',order_detail, name='order_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

