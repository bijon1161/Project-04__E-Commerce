from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginView, home_page, RegisterView, about_page, contact_page, guest_register
# from .views import about_page, contact_page
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view


urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('checkout/address/create', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/guest', guest_register, name='guest_register'),

    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('cart/', include('carts.urls', namespace='cart')),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),

    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
