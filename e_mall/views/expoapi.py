from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, auth
from e_mall.forms.usersignup import MyCustomSignupForm
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from e_mall.models.userprofile import User
from e_mall.models.products import Products
from e_mall.models.userprofile import *
from e_mall.models.location import *
from e_mall.serializer import ProductsSerializer,ProductSerializer, AdvertisementSerializer, CountrySerializer, LocationSerializer, UserSerializer
from rest_framework.views import APIView
from .page_nate import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models.functions import Replace, Cast
from django.db.models import Value, CharField
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class HomePageAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            international = Products.objects.filter(international=True).order_by('-id')
            international = intpagey(results_item=international, request_item=request)
        except:
            international = None

        try:
            top_ad = Advertisements.objects.all()
        except:
            top_ad = None

        try:
            products = Products.get_all_products().order_by('-id')
        except:
            products = None

        try:
            user = User.objects.get(username=request.user)
            following22 = ProfileFollow.objects.filter(follower=user).values_list('followed', flat=True)
            following_products = Products.objects.filter(seller__in=following22).order_by('-id')
        except:
            following_products = None

        mystuff = request.GET.get('user')
        if mystuff:
            products = following_products
            signal = 'signal'
            pagination_url = f'/home?user={mystuff}&page='
            request.session['Item'] = pagination_url
            international = None
        else:
            pagination_url = '?page='
            request.session['Item'] = {}
            signal = None

        mya = request.GET.get('all')
        if mya:
            return Response({'redirect': '/store'}, status=status.HTTP_302_FOUND)

        homesignal = 'homesignals'

        countries = Country.objects.all().order_by('name')
        selected_country_id = request.GET.get('country')
        if selected_country_id:
            somelocation = Location.objects.filter(country_id=selected_country_id)
        else:
            somelocation = Location.objects.none()

        paginator = Paginator(products, 10)  # Show 10 results per page
        page_number = request.GET.get('page', 1)
        products = paginator.get_page(page_number)

        data = {
            'international': ProductSerializer(international, many=True).data if international else [],
            'countries': CountrySerializer(countries, many=True).data,
            'selected_country_id': selected_country_id,
            'top_ad': AdvertisementSerializer(top_ad, many=True).data if top_ad else [],
            'homesignal': homesignal,
            'signal': signal,
            'following_products': ProductSerializer(following_products, many=True).data if following_products else [],
            'products': ProductSerializer(products, many=True).data,
            'has_next':products.has_next(),
            'location': LocationSerializer(somelocation, many=True).data,
        }

        

        return Response(data)
    

def api_product_details(request, products_id):
    product_item = get_object_or_404(Products, slug=products_id)
    choso = product_item.category
    try:
        subscribed_user = Subscription.objects.get(user=product_item.seller)
    except Subscription.DoesNotExist:
        subscribed_user = None

    response_data = {
        'id': product_item.id,
        'name': product_item.name,
        'description': product_item.description,
        'price': product_item.price,
        'image_url': product_item.image1.url if product_item.image1 else None,
        'image_url2': product_item.image2.url if product_item.image2 else None,
        'image_url3': product_item.image3.url if product_item.image3 else None,
        'image_url4': product_item.image4.url if product_item.image4 else None,
        'image_url5': product_item.image5.url if product_item.image5 else None,
        'image_url6': product_item.image6.url if product_item.image6 else None,
        'image_url7': product_item.image7.url if product_item.image7 else None,
        'image_url8': product_item.image8.url if product_item.image8 else None,
        'image_url9': product_item.image9.url if product_item.image9 else None,
        'image_url10': product_item.image10.url if product_item.image10 else None,
        'category': choso.name if choso else None,
        'location':product_item.location.name if product_item.location else None,
        'seller': {
            'username': product_item.seller.username,
            'email': product_item.seller.email,
            'is_subscribed': bool(subscribed_user)
        }
    }
    return JsonResponse(response_data)

class PostProductAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if Products.objects.filter(seller=request.user).count() >= 10:
            return Response({"error": "You've reached your post limit!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(seller=request.user)
            return Response({"success": "Product posted successfully!", "product": ProductsSerializer(product).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def api_signup(request):
    if request.method == 'POST':
        form = MyCustomSignupForm(request.data)
        if form.is_valid():
            user = form.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login API
def get_auth_for_user(user):

    return {
        'user':UserSerializer(user).data
    }

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(status=400)
        user=authenticate(username=username, password=password)
        if not user:
            return Response(status=401)
        
        user_data = get_auth_for_user(user)

        return Response(user_data)

# User Logout API
@csrf_exempt
@api_view(['POST'])
def api_logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)

def api_search_results(request, **kwargs):
    query = request.GET.get('q')
    if query:
        newproducts = Products.objects.annotate(
            name_no_whitespace=Replace('name', Value(' '), Value('')),
            description_no_whitespace=Cast(Replace('description', Value(' '), Value('')), output_field=CharField())
        )
        query_words = query.split()
        queries = [
            models.Q(name_no_whitespace__icontains=word.lower()) |
            models.Q(description_no_whitespace__icontains=word.lower()) for word in query_words
        ]
        quarrel = models.Q()
        for qq in queries:
            quarrel &= qq
        results = newproducts.filter(quarrel).order_by('-id')

        # Paginate the results
        paginator = Paginator(results, 10)  # Show 10 results per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Serialize results
        serialized_results = [{
            'name': product.name,
            'description': product.description,
            'location': product.location.name if product.location else None,
            'country': product.location.country.name if product.location else None,
            'image_url': product.image1.url if product.image1 else None,
            'category':product.category.verbose_name if product.category.verbose_name else product.category.name ,
            'id': product.id,
            'slug':product.slug,
        } for product in page_obj]

        response_data = {
            'results': serialized_results,
            'has_next': page_obj.has_next(),
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)

@requires_csrf_token
def api_user_catalog(request, seller_id):
    sell_products = get_object_or_404(User, username=seller_id)
    sell_id = sell_products.id
    user_products = Products.objects.filter(seller=sell_id).order_by('-id')

    # Get user profile information
    try:
        user_about = Profile.objects.get(username=sell_id)
    except Profile.DoesNotExist:
        user_about = None

    # Subscription info
    try:
        subscribed_user = Subscription.objects.get(user=sell_id)
        post_limito = subscribed_user.plan.post_limit
        posts_left = post_limito - Products.objects.filter(seller=sell_id).count()
        days_left = (subscribed_user.end_date - timezone.datetime.now()).days
        days_left = days_left if days_left < 6 else None
    except Subscription.DoesNotExist:
        subscribed_user = None
        post_limito = None
        posts_left = None
        days_left = None

    # Followers and following lists
    try:
        howfar = User.objects.get(username=request.user)
        followers = howfar.followers.all()
        following = ProfileFollow.objects.filter(follower=howfar).values_list('followed__username', flat=True)
        following22 = ProfileFollow.objects.filter(follower=howfar).values_list('followed', flat=True)
        following_products = Products.objects.filter(seller__in=following22).order_by('-id')
    except:
        following_products = None
        following = None
        followers = None

    # Prepare response data
    response_data = {
        'user': {
            'username': sell_products.username,
            'about': user_about.about if user_about else None,
            'posts_left': posts_left,
            'post_limit': post_limito,
            'days_left': days_left,
            'followers_count': followers.count() if followers else 0,
            'following_count': len(following) if following else 0,
        },
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image1.url if product.image1 else None,
                'slug':product.slug,
            }
            for product in user_products
        ],
        'following_products': [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image1.url if product.image1 else None,
            }
            for product in following_products
        ] if following_products else []
    }

    return JsonResponse(response_data, safe=False)
