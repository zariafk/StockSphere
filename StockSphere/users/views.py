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
from .models import Resource, Product
from .serializers import ResourceSerializer, ProductSerializer

# AUTHENTICATION
@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})

@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON'}, status=400
        )

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse(
        {'success': False, 'message': 'Invalid credentials'}, status=401
    )

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