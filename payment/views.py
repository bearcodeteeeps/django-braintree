from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from models import Subscription
from django.conf import settings

# Create your views here.


@method_decorator(login_required, name='dispatch')
class PaymentView(View):
    def post(self, request, *list, **kwargs):
        print "Request received"
        operation = request.POST['operation'].lower()
        plan_name = request.POST['plan_name'].lower()
        print operation, plan_name


        if operation.lower() == 'create':
            subscription = Subscription.create_subscription(request.user, plan_name, nonce=request.POST["nonce"])
            data = {}
            if subscription:
                data['success'] = True
                data['redirect'] = settings.BRAINTREE_SUCCESS_URL
                return JsonResponse(data= data, status=200, content_type="application/json")
            else:
                data['success'] = False
                data['redirect'] = settings.BRAINTREE_FAIL_URL
                return JsonResponse(data=data, status=200, content_type="application/json")
        elif operation.lower() == 'delete':
            return JsonResponse(data={}, status=200, content_type="application/json")



paymentview = PaymentView.as_view()

