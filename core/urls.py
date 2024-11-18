from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
  
    path('data/', view=views.dashboard ),
     path('admin/login/', LoginView.as_view(), name='login'),
    path('categories/', views.product_category_chart, name='category'),
    path('payment-sector/', views.get_payment_method_counts, name='payment'),
    path('gender-doughnut/', views.get_gender_percentages, name='gender'),
    path('device-types/', views.get_device_type_counts, name='device')

]

