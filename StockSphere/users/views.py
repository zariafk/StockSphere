import random

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resource, Product, Delivery, DeliveryResource, Notification, Post, Community, Comment
from .serializers import ResourceSerializer, ProductSerializer, DeliverySerializer, PostSerializer, CommentSerializer, CommunitySerializer
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework import status

from django.template.loader import get_template
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

try:
    template = get_template('password-reset-email.html')
    print("Template found!")
except Exception as e:
    print("Error: ", e)


# AUTHENTICATION
@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    return JsonResponse({'message': 'CSRF cookie set'})

from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

def password_reset_request(request):
    if request.method == "POST":
        try:
            # Ensure the request body is JSON
            import json
            body = json.loads(request.body.decode('utf-8'))
            email = body.get('email', None)

            # Check if the email is provided
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            # Use PasswordResetForm to validate the email
            form = PasswordResetForm(data={'email': email})
            if form.is_valid():
                # If email is valid, send the reset link
                users = list(form.get_users(email))  # Convert the generator to a list
                if users:
                    user = users[0]  # Now you can safely access the first user
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(str(user.pk).encode())

                    # Construct the password reset URL
                    reset_link = f'http://localhost:8000/password_reset_confirm/{uid}/{token}'

                    # Send the password reset email
                    send_mail(
                        'Password Reset Request',
                        f'Click the following link to reset your password: {reset_link}',
                        'no-reply@example.com',
                        [email],
                        fail_silently=False,
                    )
                    return JsonResponse({'message': 'Check your email for a reset link.'}, status=200)
                else:
                    return JsonResponse({'error': 'No user found with this email address.'}, status=400)

            else:
                # If form is invalid (email not found, etc.)
                return JsonResponse({'error': 'Invalid email address or user does not exist.'}, status=400)

        except json.JSONDecodeError:
            # Handle case where JSON is not properly formatted
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the UID from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('password_reset_complete')
            else:
                form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form})

        else:
            return JsonResponse({'error': 'The reset link is invalid or expired.'}, status=400)

    except Exception as e:
        return JsonResponse({'error': 'Invalid reset link.'}, status=400)


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')
    
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
    

# Fetch notifications for the logged-in user
@require_http_methods(['GET'])
def fetch_notifications(request):
    # Manual authentication check
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    # Fetch unread notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    notifications_data = [
        {
            'id': notification.id,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at,
        }
        for notification in notifications
    ]
    return JsonResponse(notifications_data, safe=False)


# Save a new notification
@require_http_methods(['POST'])
def save_notification(request):
    # Manual authentication check
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('userId')
            message = data.get('message')
            is_read = data.get('is_read', False)

            # Create and save the notification
            notification = Notification(user_id=user_id, message=message, is_read=is_read)
            notification.save()

            return JsonResponse({"message": "Notification saved successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# Dashboard: Fetch and save notifications
# If CSRF is enabled, remove this.
@require_http_methods(['GET', 'POST'])
def dashboard(request):
    # Manual authentication check
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body)
            user_id = data.get('userId')
            message = data.get('message')
            is_read = data.get('is_read', False)

            # Check for missing required fields
            if not user_id or not message:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Retrieve the user object based on username (since you're sending username as userId)
            user = User.objects.get(username=user_id)

            # Create and save the notification
            notification = Notification(user=user, message=message, is_read=is_read)
            notification.save()

            return JsonResponse({"message": "Notification saved successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'GET':
        # Fetch notifications for the logged-in user
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        notifications_data = [
            {
                'id': notification.id,
                'message': notification.message,
                'is_read': notification.is_read,
                'created_at': notification.created_at,
            }
            for notification in notifications
        ]
        return JsonResponse(notifications_data, safe=False)

@require_http_methods(['PUT'])
@login_required
def mark_notification_as_read(request, notification_id):
    # Fetch the notification by ID
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    # Mark the notification as read
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'Notification marked as read'}, status=200)

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

        # Re-serialize and return updated delivery
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
    

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    
    def perform_create(self, serializer):
        # Automatically set the 'created_by' field to the currently authenticated user
        serializer.save(created_by=self.request.user)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    print ('PostViewSet is hit!')
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  

    def retrieve(self, request, *args, **kwargs):
        print("Retrieve method hit!")  # Log if the retrieve method is hit
        return super().retrieve(request, *args, **kwargs)

    # Default create method provided by DRF, but you can modify it if you need
    def create(self, request, *args, **kwargs):
        # Print the user data
        print("create inside PostViewSet Hit!")
        if request.user.is_authenticated:
            print(f"Authenticated User: {request.user.username}")  # Log the authenticated user's username
        else:
            print("User is not authenticated!")  # Log if the user is not authenticated

        # Manually set the 'author' field to the current logged-in user
        data = request.data.copy()  # Make a copy to modify
        data['author'] = request.user.id  # Add the author field
        data['community'] = int(data.get('community'))  # Ensure community ID is an integer

        print(f"Post Data: {data}")  # Log data to verify if 'author' is being set correctly

        # Pass the modified data to the serializer
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            # Create the post instance and save
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f"Serializer errors: {serializer.errors}")  # Log serializer errors if validation fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        post_id = self.kwargs.get('pk')  # Get the post ID from the URL
        print(f"Fetching post with ID: {post_id}")  # Log the ID
        
        try:
            obj = Post.objects.get(id=post_id)  # Explicitly query the database for the post
            print(f"Retrieved post: {obj}")  # Print the retrieved post object
        except Post.DoesNotExist:
            print(f"Post with ID {post_id} does not exist.")  # Log if post does not exist
            raise  # Let the default DRF exception handler catch this and return a 404

        return obj
    
    # Action to get the post and its comments (replies)
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()  # Get the specific post
        comments = Comment.objects.filter(post=post)  # Get comments related to the post
        serializer = CommentSerializer(comments, many=True)  # Serialize the comments
        return Response(serializer.data)  # Return comments as a response

    # Action to create a new comment (reply) to a post
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()  # Get the post to which the comment is being added
        content = request.data.get('content', '')  # Get the content of the comment
        
        # Ensure content is not empty
        if not content:
            return Response({"detail": "Content cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the new comment
        comment = Comment.objects.create(
            post=post,  # Associate the comment with the post
            author=request.user,  # Set the current logged-in user as the author
            content=content  # The content of the comment
        )
        
        # Serialize and return the newly created comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
