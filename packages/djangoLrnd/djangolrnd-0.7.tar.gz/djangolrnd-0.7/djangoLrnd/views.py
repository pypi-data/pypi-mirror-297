from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.apps import apps
from .middleware import LRNDMiddleware

class ValidateView(View):
    template_name = 'djangoLrnd/validate.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        key = request.POST.get('key')
        if not key:
            messages.error(request, 'Please provide a key.')
            return render(request, self.template_name)

        response = LRNDMiddleware.check_key_status(key)
        if response.status_code == 200:
            LRNDKey = apps.get_model('djangoLrnd', 'LRNDKey')
            LRNDKey.objects.update_or_create(id=1, defaults={'key': key})
            messages.success(request, 'Key validated successfully.')
            success_redirect_url = getattr(settings, 'LRND_SUCCESS_REDIRECT_URL', 'home')
            return redirect(success_redirect_url)
        else:
            messages.error(request, 'Invalid key. Please try again.')
            return render(request, self.template_name)

validate_view = ValidateView.as_view()