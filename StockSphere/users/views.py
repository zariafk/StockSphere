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
from .models import Resource
from .serializers import ResourceSerializer

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
    

# PRODUCTS
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
    """
    Add a new product linked to the authenticated user.
    """
    try:
        data = json.loads(request.body)
        serializer = ResourceSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign product to logged-in user
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)