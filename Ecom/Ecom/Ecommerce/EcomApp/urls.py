from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('proDetail/<int:pid>',views.proDetail,name='productDetail'),
    path('viewCart/',views.viewCart,name='viewCart'),
    path('addCart/<int:pid>',views.add_cart,name='addCart'),
    path('removeCart/<int:pid>',views.removeCart,name='removeCart'),
    path('search/',views.product_search, name='product_search'),
    path('products/all',views.all_products, name='all_products'),
    path('products/watches',views.watches, name='watches'),
    path('products/Mobile',views.Mobile, name='Mobile'),
    path('products/Laptop',views.Laptop, name='Laptop'),
    path('range/',views.range, name='range'),
    path('sort-high-to-low/', views.product_list_high_to_low, name='product_list_high_to_low'),
    path('sort-low-to-high/', views.product_list_low_to_high, name='product_list_low_to_high'),
    path("updateqty/<int:uval>/<int:pid>",views.updateqty,name="updateqty"),
    path('register/',views.register_user,name="register"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('viewOrder/',views.viewOrder,name='viewOrder'),
    path('makepayment/',views.makepayment,name='makepayment'),
]