from django.views import View
from products.models import Orders
from django.shortcuts import render
from django.db.models import Count

class ProductVisualisation(View):
    def get(self, request):
        order_counts = (Orders.objects
                       .values('payment_date')  # Group by date
                       .annotate(count=Count('id'))  # Count orders per date
                       .order_by('payment_date'))  # Sort by date
        
        # Extract dates and counts for the chart
        dates = [order['payment_detail'].strftime('%Y-%m-%d') for order in order_counts]
        counts = [order['count'] for order in order_counts]
        
        return render(request, 'dashboards/orders.html', {
            'order_details': counts,
            'payment_dates': dates
        })

        