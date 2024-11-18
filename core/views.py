from django.shortcuts import render
from .models import Order
from django.db.models import Sum
import plotly.express as px
from django.db.models import Count#+
from django.shortcuts import render
from .models import Order  # Replace with your actual model if necessary
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def dashboard(request):
    # Get distinct categories and products from the database (adjust model and field names)
    categories = Order.objects.values_list('product_category', flat=True).distinct()
    products = Order.objects.values_list('product', flat=True).distinct()

    # Filter orders based on the selected filters
    category_filter = request.GET.get('category')
    product_filter = request.GET.get('product')
    gender_filter = request.GET.get('gender')

    orders = Order.objects.all()

    if category_filter:
        orders = orders.filter(product_category=category_filter)
    if product_filter:
        orders = orders.filter(product=product_filter)
    if gender_filter:
        orders = orders.filter(gender=gender_filter)

    # Pass the filtered orders, categories, and products to the template
    return render(
        request,
        'dashboard.html',
        {
            'orders': orders,
            'categories': categories,
            'products': products,
        }
    )


def product_category_chart(request):
    # Query to get product categories and their respective counts
    category_counts = Order.objects.values('product_category')\
                                    .annotate(count=Count('product_category'))\
                                    .order_by('product_category')

    # Extract labels (categories) and values (counts) separately
    labels = [category['product_category'] for category in category_counts]
    values = [category['count'] for category in category_counts]

    # Pass the labels and values as context
    return render(request, 'categories_bar.html', {
        'labels': labels,
        'values': values
    })


def get_payment_method_counts(request):
    # Query to get payment methods and their respective counts
    payment_counts = Order.objects.values('payment_method')\
                                  .annotate(count=Count('payment_method'))\
                                  .order_by('payment_method')

    # Extract labels (payment methods) and values (counts) separately
    labels = [payment['payment_method'] for payment in payment_counts]
    values = [payment['count'] for payment in payment_counts]

    

    # Return the labels and values in JSON format for use in a chart or table
    return render(request, 'payment_method_sector.html',{
        'labels': labels,
        'values': values
    })


def get_gender_percentages(request):
    # Query to count occurrences of each gender
    gender_counts = Order.objects.values('gender')\
                                 .annotate(count=Count('gender'))

    # Calculate total count
    total_count = sum([entry['count'] for entry in gender_counts])

    # Calculate percentages and prepare labels and values
    labels = [entry['gender'] for entry in gender_counts]
    values = [(entry['count'] / total_count) * 100 if total_count > 0 else 0 for entry in gender_counts]

    # Return the labels and values in JSON format
    return render(request,'gender_donut.html',{
        'labels': labels,
        'values': values
    })


def get_device_type_counts(request):
    # Query to count occurrences of each device type
    device_type_counts = Order.objects.values('device_type')\
                                      .annotate(count=Count('device_type'))\
                                      .order_by('device_type')

    # Prepare labels and values
    labels = [entry['device_type'] for entry in device_type_counts]
    values = [entry['count'] for entry in device_type_counts]

    # Return the labels and values in JSON format
    return render(request, 'device_type_bar.html',{
        'labels': labels,
        'values': values
    })
