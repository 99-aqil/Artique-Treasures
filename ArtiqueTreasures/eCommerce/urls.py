from django.urls import path

from . import views, apis

urlpatterns = [
    path('', views.loginView, name='login-page'),
    path('registration/', views.registrationView, name='register-page'),
    path('logout/', views.logoutView, name='logout'),
    path('add-to-cart/<int:product_id>/<int:user_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/<int:pk>/', views.cart_view, name='cart-view'),
    path('clear-cart/<int:pk>/', views.clear_cart, name='clear-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('products/', views.product_list, name='product-list'),
    path('products/adminUpdate/<int:pk>/', views.admin_product_update, name='admin-product-update'),
    path('products/<int:pk>/', views.product_detail, name='detail-product'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/update/<int:pk>/', views.product_update, name='product-update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product-delete'),


    path('login/', apis.UserLoginAPIView.as_view(), name='login'),
    path('register/', apis.UserRegistrationAPIView.as_view(), name='register'),
    path('customerInfo/<int:pk>/', apis.CustomerInfoAPI.as_view(), name="customer-info"),
    path('adminView/', apis.AdminViewAPI.as_view(), name='admin-view'),
    path('sellerView/', apis.SellerViewAPI.as_view(), name='seller-view'),
    path('customerView/<int:pk>/', apis.CustomerViewAPI.as_view(), name='customer-view'),
    path('search/<int:pk>/', apis.search, name="search"),
    path('productDetail/<int:product_id>/<int:user_id>/', apis.ProductDetailAPI.as_view(), name="product-detail"),
    path('artCategory/<int:pk>/', apis.ArtCategoryView.as_view(), name="art-category"),
    path('antiqueCategory/<int:pk>/', apis.AntiqueCategoryView.as_view(), name="antique-category"),
]