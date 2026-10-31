import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Order, SampleRequest
# store/views.py update
from django.shortcuts import render
from .models import Product
import json
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from django.shortcuts import render, get_object_or_404
from .models import Order

def order_success_view(request, tracking_id):
    order = get_object_or_404(Order, tracking_id=tracking_id)
    return render(request, 'store/order_success.html', {'order': order})

@csrf_exempt
def checkout_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            full_name = data.get('full_name')
            phone_number = data.get('phone_number')
            city = data.get('city')
            address = data.get('address')
            cart_items = data.get('items', [])

            if not cart_items:
                return JsonResponse({'success': False, 'error': 'Cart is empty!'})

            # Total amount calculate karein
            total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
            
            # Unique Tracking ID generate karein (Misal ke tor par: SNC-84920)
            tracking_id = f"SNC-{random.randint(10000, 99999)}"

            # Order object banayein
            order = Order.objects.create(
                tracking_id=tracking_id,
                full_name=full_name,
                phone_number=phone_number,
                city=city,
                address=address,
                total_amount=total_amount,
                status='Pending',
                is_b2b_order=False
            )

            # Cart ke har item ko OrderItem mein save karein
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            return JsonResponse({'success': True, 'tracking_id': tracking_id})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def home_view(request):
    # Consumer Packs (6-pack, 12-pack, Gift Boxes, Flavor Samplers)
    retail_packs = Product.objects.filter(product_type='retail')
    
    # Wholesale Cartons (50+ units, Commercial Boxes)
    bulk_boxes = Product.objects.filter(product_type='bulk')
    
    context = {
        'retail_packs': retail_packs,
        'bulk_boxes': bulk_boxes,
    }
    return render(request, 'store/home.html', context)

def home(request):
    retail_products = Product.objects.filter(product_type='retail')
    bulk_products = Product.objects.filter(product_type='bulk')
    context = {
        'retail_products': retail_products,
        'bulk_products': bulk_products,
        'plastic_saved': 14890,
    }
    return render(request, 'store/home.html', context)

def b2b_hub(request):
    if request.method == 'POST':
        cafe_name = request.POST.get('cafe_name')
        contact_person = request.POST.get('contact_person')
        city = request.POST.get('city')
        usage = request.POST.get('estimated_usage')

        SampleRequest.objects.create(
            cafe_name=cafe_name,
            contact_person=contact_person,
            city=city,
            estimated_usage=usage
        )
        messages.success(request, "Your Sample Kit Request has been submitted! Our commercial team will contact you within 2 hours.")
        return redirect('b2b_hub')

    bulk_products = Product.objects.all()
    return render(request, 'store/b2b_hub.html', {'products': bulk_products})

def track_order(request):
    order = None
    query = request.GET.get('tracking_id')
    if query:
        order = Order.objects.filter(tracking_id__iexact=query).first()
    return render(request, 'store/track_order.html', {'order': order, 'query': query})