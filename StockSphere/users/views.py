import random

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resource, Product, Delivery, DeliveryResource
from .serializers import ResourceSerializer, ProductSerializer, DeliverySerializer
from django.core.mail import send_mail
from django.contrib.auth.models import User

# AUTHENTICATION
@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    return JsonResponse({'message': 'CSRF cookie set'})

@require_http_methods(['POST'])
@csrf_exempt
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user:
        # Generate 6-digit code
        code = random.randint(100000, 999999)

        # Store 2FA info in session
        request.session['2fa_user_id'] = user.id
        request.session['2fa_code'] = str(code)
        request.session.modified = True


        # Send email with 2FA code
        send_mail(
            'Your 2FA Code',
            f'Your verification code is: {code}',
            'noreply@yourdomain.com',  # Or your Gmail address
            [user.email],
            fail_silently=False,
        )

        return JsonResponse({'success': True, 'message': '2FA code sent to email'})
    
    return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)

@require_http_methods(['POST'])
@csrf_exempt
def verify_2fa_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    user_id = request.session.get('2fa_user_id')
    stored_code = request.session.get('2fa_code')

    if not user_id or not stored_code:
        return JsonResponse({'success': False, 'message': '2FA session expired'}, status=403)

    if str(code) == stored_code:
        user = User.objects.get(id=user_id)
        login(request, user)

        # Clear the session
        del request.session['2fa_user_id']
        del request.session['2fa_code']

        return JsonResponse({'success': True, 'message': '2FA verified'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid verification code'}, status=403)


def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})

@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {'username': request.user.username}
        )
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )

@require_http_methods(['POST'])
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)
    

# RESOURCES
@require_http_methods(['GET'])
@login_required
def get_resources(request):
    """
    Fetch only the resources that belong to the authenticated user.
    """
    resources = Resource.objects.filter(user=request.user)  # Get only the logged-in user's products
    serializer = ResourceSerializer(resources, many=True)
    return JsonResponse(serializer.data, safe=False)


@require_http_methods(['POST'])
@login_required
def add_resource(request):
    print("add resource view was hit")
    """
    Add a new product linked to the authenticated user.
    """
    try:
        data = json.loads(request.body)
        serializer = ResourceSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign product to logged-in user
            return JsonResponse(serializer.data, status=201)
        print("Validation errors: ", serializer.errors)
        return JsonResponse(serializer.errors, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@require_http_methods(['PUT'])
@login_required
def update_resource(request, resource_id):
    try:
        resource = get_object_or_404(Resource, id=resource_id, user=request.user)
        data = json.loads(request.body)
        serializer = ResourceSerializer(resource, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(['DELETE'])
@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, user=request.user)
    resource.delete()
    return JsonResponse({'message': 'Deleted'}, status=204)


# Fetch products
@require_http_methods(['GET'])
@login_required
def get_products(request):
    """
    Fetch products that belong to the authenticated user.
    """
    products = Product.objects.filter(user=request.user)  # Fetch products related to the logged-in user
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)

# Add a new product
@require_http_methods(['POST'])
@login_required
def add_product(request):
    """
    Add a new product linked to the authenticated user.
    """
    try:
        data = json.loads(request.body)
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Link the product to the logged-in user
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Update a product
@require_http_methods(['PUT'])
@login_required
def update_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id, user=request.user)
        data = json.loads(request.body)
        serializer = ProductSerializer(product, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Delete a product
@require_http_methods(['DELETE'])
@login_required
def delete_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id, user=request.user)
        product.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=204)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# Fetch deliveries
@require_http_methods(['GET'])
@login_required
def get_deliveries(request):
    deliveries = Delivery.objects.filter(user=request.user).order_by('-id')
    serializer = DeliverySerializer(deliveries, many=True)
    return JsonResponse(serializer.data, safe=False)

# Add a delivery
@require_http_methods(['POST'])
@login_required
def add_delivery(request):
    try:
        data = json.loads(request.body)
        serializer = DeliverySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@require_http_methods(['PUT'])
@login_required
def update_delivery(request, delivery_id):
    try:
        delivery = get_object_or_404(Delivery, id=delivery_id, user=request.user)
        data = json.loads(request.body)

        # Only update simple fields manually
        delivery.from_location = data.get('from_location', delivery.from_location)
        delivery.notes = data.get('notes', delivery.notes)
        delivery.completed = data.get('completed', delivery.completed)
        delivery.save()

        # 🛠 Handle resources separately
        if 'resources' in data:
            delivery.resources.all().delete()
            for res_data in data['resources']:
                DeliveryResource.objects.create(
                    delivery=delivery,
                    resource_id=res_data['resource'],
                    cases=res_data['cases']
                )

        # ✅ Re-serialize and return updated delivery
        updated_delivery_data = DeliverySerializer(delivery).data

        return JsonResponse(updated_delivery_data, status=200)

    except Exception as e:
        print('Error in update_delivery:', e)
        return JsonResponse({'error': str(e)}, status=500)




# Delete a delivery
@require_http_methods(['DELETE'])
@login_required
def delete_delivery(request, delivery_id):
    try:
        delivery = get_object_or_404(Delivery, id=delivery_id, user=request.user)
        delivery.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=204)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
