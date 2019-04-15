from django.urls import re_path
from agency import invoice_views

urlpatterns = [
  re_path(r'^search', invoice_views.InvoiceSearch.as_view()),
]
