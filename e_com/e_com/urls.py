from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from e_app.views import admin_login,logout_view,admin_home,registerView,loginView,homeView,logoutView,add_product,product_list,admin_product_list,delete_product,update_product,vieworders,update_order_status,create_order_user,cart_detail,userProfile,Cart_review,create_order,list_orders,user_order_details,remove_from_cart,add_to_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login',admin_login),
    path('admin_logout',logout_view),
    path('home',admin_home),
    path('',registerView,name='registration'),
    path('login/',loginView),
    path('homeuser',homeView),
    path('logout',logoutView),
    path('add_product',add_product),
    path('product_list',product_list),
    path('admin_product_list',admin_product_list),
    path('delete_product/<int:product_id>',delete_product),
    path('update_product/<int:product_id>',update_product),
    path('view_orders',vieworders),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('order/<int:product_id>/',create_order_user, name='create_order_user'),
    path('add-to-cart/<int:product_id>',add_to_cart),
    path('cart',cart_detail),
    path('profile',userProfile),
    path('cart_review/<int:user_id>',Cart_review,name='cart_review'),
    path('create-order/', create_order, name='create_order'),
    path('orders/', list_orders, name='list_orders'),
    path('orders/<str:order_id>/', user_order_details, name='order_details'),
    path('cart/remove/<int:product_id>/',remove_from_cart, name='remove_from_cart'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

