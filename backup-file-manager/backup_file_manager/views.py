from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {
        })


class APIRootView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    swagger_schema = None

    def get_view_name(self):
        return "API Root"

    def get(self, request, format=None):
        return Response(OrderedDict((
            ('file_manager', reverse('file_manager-api:api-root', request=request, format=format)),
        )))
