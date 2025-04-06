from django.views import View
from products.models import Orders
from django.shortcuts import render
from django.db.models import Count
import json

class ProductVisualisation(View):
    def get(self, request):
        order_counts = (Orders.objects
                       .values('timestamp')  # Group by date
                       .annotate(count=Count('id'))  # Count orders per date
                       .order_by('payment_date'))  # Sort by date
        
        # Extract dates and counts for the chart
        dates = [order['timestamp'].strftime('%Y-%m-%d') for order in order_counts]
        counts = [order['count'] for order in order_counts]
        if request.user.is_staff:

            return render(request, 'dashboards/orders.html', {
            'order_details': json.dumps(counts),
            'payment_dates': json.dumps(dates)
            })
        else:
            return render ('unauthorized')

        