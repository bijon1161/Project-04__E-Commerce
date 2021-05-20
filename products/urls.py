from django.urls import path
from products.views import (
    ProductListView,
    ProductDetailView,
    ProductDetailSlugView,
    ProductFeaturedListView,
    ProductFeaturedDetailView
)

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    # path('featured', ProductFeaturedListView.as_view()),
    # path('<int:pk>', ProductDetailView.as_view()),
    path('<slug>', ProductDetailSlugView.as_view(), name='detail'),
    # path('featured/<int:pk>', ProductFeaturedDetailView.as_view()),
]