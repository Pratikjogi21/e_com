from .user_views import registerView,homeView,loginView,logoutView
from .user_product_views import product_list
from .user_order_views import create_order_user
from .cart_views import add_to_cart,cart_detail,remove_from_cart
from .user_profile import userProfile
# from .review_cart import Cart_review,confirm_order_cart
from .review_cart import user_order_details,list_orders,create_order,Cart_review

from .admin_views import admin_home,admin_login,logout_view
from .product_views import add_product,admin_product_list,delete_product,update_product
# from .order_views import create_order,order_detail,update_order_status,vieworders
from .order_views import order_detail,update_order_status,vieworders
