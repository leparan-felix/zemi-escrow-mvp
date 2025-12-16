from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment, hash_phone, generate_delivery_code
from .services import mpesa
import random
import string

def generate_order_reference():
    return 'ZEMI-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# -----------------------------
# Core Endpoints
# -----------------------------
@csrf_exempt
@api_view(['POST'])
def create_order(request):
    data = request.data
    phone = data.get('phone')
    amount = data.get('amount')
    product_description = data.get('product_description')
    
    if not phone or not amount or not product_description:
        return Response({'error': 'Missing fields'}, status=400)
    
    order = Order.objects.create(
        order_reference=generate_order_reference(),
        phone_hashed=hash_phone(phone),
        amount=amount,
        product_description=product_description,
        delivery_code=generate_delivery_code()
    )
    return Response({
        'order_reference': order.order_reference,
        'status': order.status,
        'delivery_code': order.delivery_code
    })

@csrf_exempt
@api_view(['POST'])
def payment_webhook(request):
    """
    Force functional webhook for testing.
    If order does not exist, create it automatically.
    """
    data = request.data
    order_reference = data.get('order_reference') or "FORCE_TEST"
    transaction_id = data.get('transaction_id') or "TEST_TXN"

    # Get or create order to force functionality
    order, created = Order.objects.get_or_create(
        order_reference=order_reference,
        defaults={
            "phone_hashed": hash_phone("0700000000"),
            "amount": 1000,
            "product_description": "Forced test order",
            "delivery_code": "123456",
            "status": "awaiting_payment"
        }
    )

    # Avoid double payment
    if order.status != "awaiting_payment":
        return Response({'error': 'Order not awaiting payment'}, status=400)

    Payment.objects.create(order=order, transaction_id=transaction_id)
    order.status = 'paid'
    order.save()

    return Response({
        'message': 'Payment recorded successfully (forced)',
        'order_reference': order.order_reference,
        'status': order.status
    })

@csrf_exempt
@api_view(['POST'])
def confirm_delivery(request):
    data = request.data
    order_reference = data.get('order_reference')
    delivery_code = data.get('delivery_code')
    
    try:
        order = Order.objects.get(order_reference=order_reference)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
    
    if order.status != 'paid':
        return Response({'error': 'Order not paid yet'}, status=400)
    
    if order.delivery_code != delivery_code:
        return Response({'error': 'Invalid delivery code'}, status=400)
    
    order.status = 'completed'
    order.save()
    
    seller_phone = "0700000000"  # For MVP
    mpesa.b2c_disbursement(seller_phone, order.amount)
    
    return Response({'message': 'Delivery confirmed, funds released to seller'})

# -----------------------------
# M-Pesa Simulation
# -----------------------------
@csrf_exempt
@api_view(['POST'])
def stk_push(request):
    buyer_phone = request.data.get("buyer_phone")
    amount = request.data.get("amount")

    if not buyer_phone or not amount:
        return Response({"error": "buyer_phone and amount required"}, status=400)

    result = mpesa.initiate_stk_push(buyer_phone, amount)
    return Response(result, status=200)

@csrf_exempt
@api_view(['POST'])
def confirm_stk(request):
    transaction_ref = request.data.get("transaction_ref")
    if not transaction_ref:
        return Response({"error": "transaction_ref required"}, status=400)

    result = mpesa.confirm_stk_payment(transaction_ref)
    return Response(result, status=200)

@csrf_exempt
@api_view(['POST'])
def release_funds(request):
    seller_phone = request.data.get("seller_phone")
    amount = request.data.get("amount")
    if not seller_phone or not amount:
        return Response({"error": "seller_phone and amount required"}, status=400)

    result = mpesa.b2c_disbursement(seller_phone, amount)
    return Response(result, status=200)
