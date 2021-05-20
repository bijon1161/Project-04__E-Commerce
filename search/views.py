from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product


class SearchProductListView(ListView):
    template_name = 'search/view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            # call Product.ProductManager.Search()
            return Product.objects.search(query)
        return Product.objects.featured()
