from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import PROMO_DISCOUNTS, PurchaseForm
from .models import Product, Purchase


def index(request):
    products = Product.objects.order_by('pk')
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    form_class = PurchaseForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        return context

    def form_valid(self, form):
        discount = PROMO_DISCOUNTS.get(form.cleaned_data['promo_code'], 0)
        form.instance.product = self.product
        total = Decimal(self.product.price) * (100 - discount) / 100
        form.instance.total_price = total
        response = super().form_valid(form)
        messages.success(
            self.request, f'Покупка оформлена. К оплате {total:.2f} ₽.'
        )
        return response

