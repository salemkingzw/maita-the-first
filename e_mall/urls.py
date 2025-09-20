
from django.contrib import admin 
from django.urls import path 
from e_mall.views.home import *
from e_mall.views.signup import *
from e_mall.views.expoapi import *
from django.conf import settings
from django.conf.urls.static import static
  
app_name='e_mall'  
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('get-locations/', get_locations, name='get_locations'),
    path('get-location/<str:country_id>/', get_location, name='get_location'),
    path('',homepage,name='homepage'), 
    path('home/', store, name='store'),
    path('categories/<str:category_id>/', category_id, name='category_id'),
    path('products/<str:products_id>/', products_id, name='products_id'),       
    path('signup/', signup, name='signup'), 
    path('logout/', logout, name='logout'), 
    path('search/',search_results,name='search_results'),
    path('search/<str:location_id>/',search_results,name='search_results'),
    path('post_product/', post_product, name='post_product'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('users/<str:seller_id>/', user_catalog, name='user_catalog'),    
    path('location/<str:location_id>/', set_location, name='set_location'),
    path('location/<str:location_id>/<str:category_id>/', set_location_category, name='set_location_category'),
    path('delete_about/<int:pk>/', delete_about, name='delete_about'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('follow/<str:seller_id>/', follow_user, name='follow_user'),
    path('about_maita/', about_maita, name='about_maita'),
    path('country/<str:country_id>/', country_id, name='country_id'),
    path('api/signup/', api_signup, name='signup_api'),
    path('api/home/', HomePageAPI.as_view(), name='api_homepage'),
    path('api/login/', SignInView.as_view(), name='login_api'),
    path('api/products/<str:products_id>/', api_product_details, name='api_product_details'),
    path('api/post-product/', PostProductAPI.as_view(), name='post-product-api'),
    path('api/search/',api_search_results,name='api_search_results'),
    path('api/user_catalog/<str:seller_id>/', api_user_catalog, name='api_user_catalog'),
    #path('user_subscribe/<str:plan_id>/', user_subscribe, name='user_subscribe'),
    #path('subscription_page/',subscription_page, name='subscription_page'),    
] 
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
