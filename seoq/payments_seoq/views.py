
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, render
from payments import RedirectNeeded, get_payment_model
from plans.models import Order
from plans.views import OrderView as ParentOrderView
from plans.views import OrderPaymentReturnView as ParentReturnView


class OrderView(ParentOrderView):
    model = Order
    template_name = 'plans/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        payment, created = get_payment_model().objects.get_or_create(
            order__pk=self.object.pk,
            defaults={
                'variant': 'default',
                'description': 'Plan Purchase',
                'order': self.object,
                'total': self.object.total(),
                'tax': self.object.tax_total(),
                'currency': self.object.currency
            })
        context['payment_form'] = payment.get_form()
        context['payment'] = payment
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        try:
            context['payment_form'] = context['payment'].get_form(
                data=self.request.POST or None)
        except RedirectNeeded as redirect_to:
            return redirect(str(redirect_to))
        return render(request, self.template_name, context)


class OrderPaymentReturnView(ParentReturnView):
    """
    This view is a fallback from any payments processor. It allows just to set
    additional message context and redirect to Order view itself.
    """
    model = Order
    status = None

    def render_to_response(self, context, **response_kwargs):
        if self.status == 'success':
            messages.success(self.request,
                             _('Thank you for placing a payment. \
                                It will be processed as soon as possible.'))
        return redirect('/')
