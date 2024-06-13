from django.contrib import admin
from django.urls import path
from store.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from store.password_reset import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', SignInView.as_view(), name='sign-in'),
    path('register/', SignUpView.as_view(), name='sign-up'),
    path('owner/', AdminIndexView.as_view(), name='owner-home'),
    path('user/', UserIndexView.as_view(), name='user-home'),
    path('logout', SignOutView.as_view(), name='sign-out'),
    path('users/list/', UserListView.as_view(), name='users-list'),
    path('user/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('product/add/', CreateProductView.as_view(), name='add-product'),
    path('category/', CategoryListCreateView.as_view(), name='category'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('product/view/<int:pk>/', DetailProductView.as_view(), name='view-product'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(), name='delete-product'),
    path('product/update/<int:pk>/', UpdateProductView.as_view(), name='update-product'),
    path('cart/add/<int:pk>/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/view/', ViewCart.as_view(), name='view-cart'),
    path('cart/remove/<int:pk>', RemoveFromCart.as_view(), name='remove-item'),
    path('complaint/add/', CreateComplaint.as_view(), name='create-complaint'),
    path('complaint/view', ViewComplaints.as_view(), name='view-complaints'),
    path('complaint/delete/<int:pk>', DeleteComplaint.as_view(), name='delete-complaint'),
    path('order/view/', OrderView.as_view(), name='order-view'),
    path('order/create/', CreateOrder.as_view(), name='order-create'),
    path('order/cancel/<int:pk>/', CancelOrder.as_view(), name='cancel-order'),
    path('order/update/status/<int:pk>/', UpdateOrderStatus.as_view(), name='update-status'),
    path('payment/success/', PaymentSuccess.as_view(), name='payment-success'),
    path('user/password_reset/', PasswordResetRequestView.as_view(), name='user-password_reset'),
    path('user/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('wishlist/add/<int:pk>/',AddProductToWishList.as_view(),name='add-wishlist'),
    path('wishlist/view/',WishListView.as_view(),name='view-wishlist'),
    path('wishlist/remove/<int:pk>/',RemoveFromWishLIst.as_view(),name='remove-wishlist'),
    path('order/success/',SuccessView.as_view(),name='success'),
    path('user/profile/',UpdateProfileView.as_view(),name='update-profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
