from django.urls import path

from . import views, apis

urlpatterns = [
    path('', views.loginView, name='login-page'),
    path('registration/', views.registrationView, name='register-page'),
    path('logout/', views.logoutView, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_view, name='cart-view'),
    path('clear-cart/', views.clear_cart, name='clear-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('products/', views.product_list, name='product-list'),
    path('products/adminUpdate/<int:pk>/', views.admin_product_update, name='admin-product-update'),
    path('products/<int:pk>/', views.product_detail, name='detail-product'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/update/<int:pk>/', views.product_update, name='product-update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product-delete'),


    path('login/', apis.UserLoginAPIView.as_view(), name='login'),
    path('register/', apis.UserRegistrationAPIView.as_view(), name='register'),
    path('productsAdminView/', apis.ProductsListAdminView.as_view(), name='products-admin-view'),
    path('productsSellerView/', apis.ProductsListSellerView.as_view(), name='products-seller-view'),
    path('productsCustomerView/', apis.ProductsListCustomerView.as_view(), name='products-customer-view'),
    path('search/', apis.search, name="search"),
    path('productDetail/<int:pk>/', apis.ProductDetailAPI.as_view(), name="product-detail"),
    path('artCategory/', apis.ArtCategoryView.as_view(), name="art-category"),
    path('antiqueCategory/', apis.AntiqueCategoryView.as_view(), name="antique-category"),
]