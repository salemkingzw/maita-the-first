from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, JsonResponse
from e_mall.models.products import Products 
from e_mall.models.category import Category
from e_mall.models.location import Location, Country 
from e_mall.forms.productupload import ProductsForm
from e_mall.models.userprofile import *
from e_mall.forms.userprofileedit import ProfileForm
from django.db import models 
from django.db.models.functions import Replace, Cast
from django.db.models import Value, CharField
from .nav import *
from .page_nate import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import requires_csrf_token

def homepage(request):
    print('redirecting user to store')
    return redirect('e_mall:store')

def store(request):
    try:
        international=Products.objects.filter(international=True)
        international=international.order_by('-id')
    except:
        international=None
    try: 
        international = intpagey(results_item=international,request_item=request)    
    except:
        pass
    try:
        top_ad=Advertisements.objects.all()
    except:
        top_ad=None
    try:     
        products = Products.get_all_products() 
        products = products.order_by('-id')
    except:
        pass
    e_categories_by_order, categories_by_order = navbar()
    somelocation = loco()
    #posts from people you follow
    try:
        howfar=User.objects.get(username=request.user)
        following22=ProfileFollow.objects.filter(follower=howfar).values_list('followed',flat=True)    
        following_products=Products.objects.filter(seller__in=following22).order_by('-id')
    except:
        following_products=None    
    #diplaying posts from people you follow
    mystuff=request.GET.get('user')
    if mystuff:
        products=following_products
        signal='signal'
        pagination_url=f'/home?user={mystuff}&page='
        print('updated pagination url to',pagination_url)
        request.session['Item']=pagination_url
        international=None
    else:
        pagination_url='?page='
        request.session['Item']={}
        print('pagination url is',pagination_url)
        signal=None
    mya=request.GET.get('all')
    if mya:        
        return redirect('e_mall:store')
    #paginating index posts 
    try: 
        products = pagey(results_item=products,request_item=request)    
    except:
        pass       

    homesignal='homesignals'  
    #country based filtering
    countries = Country.objects.all().order_by('name')
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        somelocation = Location.objects.filter(country_id=selected_country_id)
    else:
        somelocation = Location.objects.none()
    ###
    data = {
        'international':international,
        'countries': countries,
        'selected_country_id': selected_country_id,
        'top_ad':top_ad,
        'homesignal':homesignal,
        'signal':signal,
        'following_products':following_products,
        'products':products,
        'location':somelocation,        
        'categories':categories_by_order,
        'electronic_category':e_categories_by_order
    }  
    request.session['current_cat']={}
    request.session['loc_cat_signal']=homesignal
    if request.headers.get('accept')=='application/json':        
        print('header accepted')
        page = request.GET.get('page', 1)
        adam=request.session.get('Item')
        if adam:
            print('got the session')
            pagination_url=adam
            print('new url is', pagination_url)
        else:
            pagination_url='?page='
            print('pagination url is',pagination_url)
        data['products']=products.paginator.get_page(str(int(page)+1))
        respondo = JsonResponse({'has_more_pages':products.has_next(),
                             'pagination_url':pagination_url,
                             'html':render_to_string('e_mall/scroll_items.html', 
                                                     data)})
        respondo['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return respondo

    return render(request, 'e_mall/index.html', data) 

def country_id(request, country_id):
    try:
        top_ad=Advertisements.objects.all()
    except:
        top_ad=None
    products = Products.objects.filter(location__country__name=country_id).order_by('-id')
    countryname = country_id
    somelocation = Location.objects.filter(country__name=country_id)
    countrynameid = Country.objects.get(name=country_id)
    countrynameid = countrynameid.pk
    #country based filtering
    countries = Country.objects.all().order_by('name')
    country_loc=country_id
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        somelocation = Location.objects.filter(country_id=selected_country_id)
    else:
        somelocation = Location.objects.filter(country_id=countrynameid)
    ###

    shipping_button=request.GET.get('shipping')
    if shipping_button:
        products=products.filter(international=True)
        countrysignalsignal='countrysignalsignal'
    else:
        countrysignalsignal=None
    all_button=request.GET.get('all')
    if all_button:
        pass

    e_categories_by_order, categories_by_order = navbar()
    try: 
        products = pagey(results_item=products,request_item=request)    
    except:
        pass 
    data ={
        'countrysignalsignal':countrysignalsignal,
        'countries': countries,
        'selected_country_id': selected_country_id,
        'location':somelocation,
        'countryname':countryname,
        'countrysignal':'countrysignal',
        'products':products,
        'top_ad':top_ad,
        'categories':categories_by_order,
    }

    if request.headers.get('accept')=='application/json':  
        page = request.GET.get('page', 1)      
        print('header accepted')            
        pagination_url=f'?page='
        print('pagination url is',pagination_url) 
        data['products']=products.paginator.get_page(str(int(page)+1))     
        respondo = JsonResponse({'has_more_pages':products.has_next(),
                            'pagination_url':pagination_url,
                            'html':render_to_string('e_mall/scroll_items.html', 
                                                    data)})
        respondo['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return respondo

    return render(request, 'e_mall/index.html', data )

def get_locations(request):
    laname=request.session.get('current_cat')
    losignal=request.session.get('loc_cat_signal')
    country_id = request.GET.get('country_id')
    somelocation = Location.objects.filter(country_id=country_id)
    templatio='e_mall/locoloco.html'
    if laname:
        navi_categoriess = get_object_or_404(Category,name=laname) 
        data={'location':somelocation, 
              'current_category':navi_categoriess,
              'locationcategorysignal':'locationcategorysignals',
              }
    elif losignal=='homesignals':
        data={'location':somelocation,
              'homesignal':'homesignals'}
    elif losignal=='countrysignal':
        data={'location':somelocation,
              'countrysignal':'countrysignal'}
    elif losignal=='locationsignals':
        data={'location':somelocation,
              'locationsignal':'locationsignals'}
    elif losignal=='searchsignal':
        data={'location':somelocation,}
        templatio='e_mall/search_results_loco.html'
    
    if request.headers.get('accept')=='application/json':        
        return JsonResponse({'html':render_to_string(templatio, 
                                                    data)})
    else:
        return redirect('e_mall:store')

def category_id(request, category_id):      
    try:
        top_ad=Advertisements.objects.all()
    except:
        top_ad=None     

    nav_categoriess = get_object_or_404(Category, name=category_id) 
    cat_id=nav_categoriess.id
    category_products= Products.get_all_products_by_categoryid(cat_id)
    category_products = category_products.order_by('-id')
    current_category = Category.objects.get(name=category_id)
    categories_signal='categories_signals'        
    e_categories_by_order, categories_by_order = navbar() 
    somelocation = loco()  

    category_products = pagey(results_item=category_products,request_item=request)
    #country based filtering
    countries = Country.objects.all()
    
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        somelocation = Location.objects.filter(country_id=selected_country_id)
    else:
        somelocation = Location.objects.none()
    ###   
    context = {
        'countries': countries,
        'top_ad':top_ad,
        'categories_signal':categories_signal,
        'location':somelocation,
        'products': category_products,
        'electronic_category':e_categories_by_order,
        'nav_categories':categories_by_order, #to give order to navigation categories
        'current_category':current_category,
    }
    #pagination using javascript
    request.session['current_cat']=category_id
    if request.headers.get('accept')=='application/json':  
        page = request.GET.get('page', 1)      
        print('header accepted')            
        pagination_url=f'?page='
        print('pagination url is',pagination_url) 
        context['products']=category_products.paginator.get_page(str(int(page)+1))     
        respondo = JsonResponse({'has_more_pages':category_products.has_next(),
                            'pagination_url':pagination_url,
                            'html':render_to_string('e_mall/scroll_category_items.html', 
                                                    context)})
        respondo['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return respondo

    return render(request, 'e_mall/categories.html', context)    

def products_id(request, products_id):
    product_item=get_object_or_404(Products, slug=products_id)
    choso=product_item.category
    try:
        subscribed_user=Subscription.objects.get(user=product_item.seller)
    except:
        subscribed_user=None
    e_categories_by_order, categories_by_order = navbar()
    context={
        #'subscribed_user':subscribed_user,
        'product_item':product_item,
        'electronic_category':e_categories_by_order,
        'categories': categories_by_order,
        'choso':choso,
    }
    return render(request, 'e_mall/products.html',context)  

def search_results(request, **kwargs):
    query=request.GET.get('q')    
    og=query
    champ=None
    #you've figured it out
    try:
        if kwargs:
            jj = request.session['querydata']    
            query=jj            
        else:
            jj=None
    except KeyError:
        pass    
    if query:
        #you genius
        request.session['querydata'] = query
        newproducts=Products.objects.annotate(name_no_whitespace=Replace('name', Value(' '), Value('')),                                             
                    description_no_whitespace=Cast(Replace('description', Value(' '), Value('')),output_field=CharField()))        
        query_words=query.split()
        queries=[models.Q(name_no_whitespace__icontains=word.lower()) |
                 models.Q(description_no_whitespace__icontains=word.lower()) for word in query_words]        
        quarrel=models.Q()
        for qq in queries:
            quarrel &= qq                                
        results=newproducts.filter(
                                quarrel)
        results=results.order_by('-id')
        #user search
        user_search=User.objects.annotate(user_no_whitespace=Replace('username', Value(' '), Value('')),)
        user_search_items=[models.Q(user_no_whitespace__icontains=word.lower()) for word in query_words]
        user_search_map=models.Q()
        for uuu in user_search_items:
            user_search_map &= uuu
        user_results=user_search.filter(user_search_map)
        user_results=user_results.order_by('-id')
        #very smart indeed
        somelocation = loco()
        if kwargs:
            for name,dd in kwargs.items():
                if dd =='all':
                    results=results
                    return redirect(f'/search/?q={query}')
                else:                    
                    champ=get_object_or_404(Location,name=dd)                    
                    results=results.filter(location__name=dd)                           
        e_categories_by_order, categories_by_order = navbar()        
        #paginating the data
        results = pagey(results_item=results,request_item=request)

        #country based filtering
        countries = Country.objects.all()
        selected_country_id = request.GET.get('country')
        if selected_country_id:
            somelocation = Location.objects.filter(country_id=selected_country_id)
        else:
            if kwargs:
                country_loc=champ.country
                somelocation = Location.objects.filter(country_id=country_loc)
            else:
                somelocation = Location.objects.none()
        ###
        request.session['loc_cat_signal']='searchsignal'
        request.session['current_cat']={}
        context={
            'countries': countries,
            'selected_country_id': selected_country_id,
            'user_results':user_results,
            'og':og,
            'current_location':champ,
            'jj':jj,
            'location':somelocation,
            'results':results,
            'electronic_category':e_categories_by_order,
            'categories': categories_by_order,
        }
            
        #paginating search results
        if request.headers.get('accept')=='application/json':
            page = request.GET.get('page', 1)            
            if kwargs:
                print('header accepted')            
                pagination_url=f'?page='
                print('pagination url is',pagination_url)
            else:
                print('header accepted')            
                pagination_url=f'?q={og}&page='
                print('pagination url is',pagination_url)
            context['results']=results.paginator.get_page(str(int(page)+1))
            respondo = JsonResponse({'has_more_pages':results.has_next(),
                                'pagination_url':pagination_url,
                                'html':render_to_string('e_mall/scroll_search_results.html', 
                                                        context)})
            respondo['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return respondo
        
        return render (request, 'e_mall/search_results.html', context)

    else:        
        return redirect('e_mall:store')

@requires_csrf_token    
@login_required
def post_product(request):
    #if Subscription.objects.filter(user=request.user).exists():
    #    subscribed_user=Subscription.objects.get(user=request.user)
    #    if ((subscribed_user.end_date)<=timezone.datetime.now()):
    #        subscribed_user.is_active=False
    #        subscribed_user.save()          
    #if Subscription.objects.filter(user=request.user,is_active=True).exists():
    #    yosef=Subscription.objects.get(user=request.user)
    #    post_limito=yosef.plan.post_limit
    #else:
    post_limito=10
    if Products.objects.filter(seller=request.user).count()<post_limito:
        if request.method == 'POST':
            form = ProductsForm(request.POST, request.FILES)        
            if form.is_valid():
                products = form.save(commit=False)
                products.seller = request.user
                u_idd=request.user
                products.save()
                return redirect('e_mall:user_catalog',u_idd)
        else:
            form = ProductsForm()
        return render (request, 'e_mall/post_product.html', {'form':form})
    else:
        request.session['lamessage']="you've reached your post limit!"
        #if Subscription.objects.filter(user=request.user).exists():
        #    useruser=Subscription.objects.get(user=request.user)
        #    if useruser.is_active==False:
        #        request.session['lamessage']=f"your plan has expired, you subscribed on {(useruser.start_date).date()}, today is {timezone.now().date()}"       
        return redirect('e_mall:user_catalog',request.user)
@requires_csrf_token
def get_location(request, country_id):
    locations = Location.objects.filter(country_id=country_id).order_by('name')
    location_data = [{"id": loc.id, "name": loc.name} for loc in locations]
    return JsonResponse({"locations": location_data})
"""
@requires_csrf_token
@login_required
def subscription_page(request):
    subscription_plans=SubscriptionPlan.objects.all()
    try:
        subscribed_plan=Subscription.objects.get(user=request.user)
        subscribed_plan=subscribed_plan.plan
    except:
        subscribed_plan=None
    ddd=request.session.get('already_subscribed')
    if ddd:
        messengilo=ddd
    else:
        messengilo=None
    e_categories_by_order, categories_by_order = navbar()
    request.session['already_subscribed']={}
    subscriptionsignal='subscriptionsignal'
    data={
        'subscriptionsignal':subscriptionsignal,
        'electronic_category':e_categories_by_order,
        'categories': categories_by_order,
        'subscribed_plan':subscribed_plan,
        'subscription_plans':subscription_plans,
        'messengilo':messengilo,
    }
    return render(request, 'e_mall/subscription_page.html', data)
@requires_csrf_token
@login_required
def user_subscribe(request, plan_id):
    if Subscription.objects.filter(user=request.user).exists():
        request.session['already_subscribed']="You are already subscribed."
        return redirect('e_mall:subscription_page')
    else:
        plan=SubscriptionPlan.objects.get(id=plan_id)   
        subscription=Subscription.objects.create(user=request.user,
                                                 plan=plan,start_date=timezone.datetime.now(),
                                                 end_date=timezone.datetime.now() + timezone.timedelta(days=30))
        subscription
        return redirect('e_mall:user_catalog', request.user)
"""
@requires_csrf_token
def user_catalog(request, seller_id):
    sell_products = get_object_or_404(User, username=seller_id) #this is a very good practice for getting stuff represented in URL
    sell_id=sell_products.id
    user_products = Products.objects.filter(seller=sell_id)
    user_products=user_products.order_by('-id')
    try:
        user_about = Profile.objects.get(username=sell_id)
    except:
        user_about=None
    bbb=request.session.get('lamessage')    
    if bbb:
        lamessage=bbb
    else:
        lamessage=None
    request.session['lamessage']={}
    try:
        subscribed_user=Subscription.objects.get(user=sell_id)
        post_limito=subscribed_user.plan.post_limit
        posts_left=post_limito-Products.objects.filter(seller=sell_id).count()
        days_left=subscribed_user.end_date-timezone.datetime.now()
        days_left=days_left.days
        if days_left<6:
            days_left=days_left  
        else:
            days_left=None
    except:
        subscribed_user=None
        post_limito=None
        posts_left=None
        days_left=None
    #followers and following list
    
    try:
        howfar=User.objects.get(username=request.user)
        followers=howfar.followers.all()
        following=ProfileFollow.objects.filter(follower=howfar).values_list('followed__username',flat=True)
        #products from people you follow
        following22=ProfileFollow.objects.filter(follower=howfar).values_list('followed',flat=True)    
        following_products=Products.objects.filter(seller__in=following22).order_by('-id')
    except:
        following_products=None
        following=None
        followers=None
    #getting urls for sharing posts
    url_d_posts=[]
    for stuff in user_products:
        absolute_url=request.build_absolute_uri(stuff.get_absolute_url())
        url_d_posts.append((stuff, absolute_url))
    e_categories_by_order, categories_by_order = navbar()
    context = {
        #'days_left':days_left,
        'url_d_posts':url_d_posts,
        'posts_left':posts_left,
        'post_limito':post_limito,
        #'subscribed_user':subscribed_user,
        'lamessage':lamessage,
        'following_products':following_products,      
        'following':following,  
        'followers':followers,
        'about':user_about,
        'products':user_products,
        'sell_products':sell_products,
        'electronic_category':e_categories_by_order,
        'nav_categories':categories_by_order, 
    }
    return render (request, 'e_mall/user_products.html', context)

def set_location(request, location_id):
    try:
        top_ad=Advertisements.objects.all()
    except:
        top_ad=None     

    location_products = get_object_or_404(Location, name=location_id) 
    location_id=location_products.id
    loc_p = Products.objects.filter(location=location_id)
    loc_p=loc_p.order_by('-id')
    locationsignal='locationsignals'
    e_categories_by_order, categories_by_order = navbar()
    somelocation = loco() 
    loc_p = pagey(results_item=loc_p,request_item=request)  
    #country based filtering
    countries = Country.objects.all()
    country_loc=location_products.country
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        somelocation = Location.objects.filter(country_id=selected_country_id)
    else:
        somelocation = Location.objects.filter(country_id=country_loc)
    ###
    context = {
        'countries': countries,
        'selected_country_id': selected_country_id,
        'top_ad':top_ad,
        'locationsignal':locationsignal,
        'products':loc_p,
        'location':somelocation,  
        'sell_products':location_products,
        'electronic_category':e_categories_by_order,
        'nav_categories':categories_by_order, 
    }
    request.session['current_cat']={}
    request.session['loc_cat_signal']=locationsignal
    #pagination using javascript
    if request.headers.get('accept')=='application/json':
        page = request.GET.get('page', 1)        
        print('header accepted')            
        pagination_url=f'?page='
        print('pagination url is',pagination_url) 
        context['products']=loc_p.paginator.get_page(str(int(page)+1))     
        respondo = JsonResponse({'has_more_pages':loc_p.has_next(),
                            'pagination_url':pagination_url,
                            'html':render_to_string('e_mall/scroll_location_index.html', 
                                                    context)})
        respondo['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return respondo
    return render (request, 'e_mall/location_index.html', context)

def set_location_category(request, location_id, category_id):
    try:
        top_ad=Advertisements.objects.all()
    except:
        top_ad=None     

    navi_categoriess = get_object_or_404(Category,name=category_id) 
    cati_id=navi_categoriess.id
    location_products = get_object_or_404(Location,name=location_id) 
    location_id=location_products.id
    loc_p = Products.objects.filter(location=location_id)
    loc_p = loc_p.filter(category=cati_id)
    loc_p=loc_p.order_by('-id')
    locationcategorysignal='locationcategorysignals'
    loc_p = pagey(results_item=loc_p,request_item=request)  
    e_categories_by_order, categories_by_order = navbar()
    somelocation = loco()
    #country based filtering
    countries = Country.objects.all()
    country_loc=location_products.country
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        somelocation = Location.objects.filter(country_id=selected_country_id)
    else:
        somelocation = Location.objects.filter(country_id=country_loc)
    ###   
    context = {
        'countries': countries,
        'top_ad':top_ad,
        'locationcategorysignal':locationcategorysignal,
        'products':loc_p,
        'location':somelocation,  
        'sell_products':location_products,
        'electronic_category':e_categories_by_order,
        'nav_categories':categories_by_order,
        'current_category':navi_categoriess 
    }
    
    request.session['loc_cat_signal']=locationcategorysignal
    request.session['current_cat']=category_id
    #pagination using javascript
    if request.headers.get('accept')=='application/json':
        page = request.GET.get('page', 1)        
        print('header accepted')            
        pagination_url=f'?page='
        print('pagination url is',pagination_url)
        context['products']=loc_p.paginator.get_page(str(int(page)+1))      
        respondo = JsonResponse({'has_more_pages':loc_p.has_next(),
                            'pagination_url':pagination_url,
                            'html':render_to_string('e_mall/scroll_location_products.html', 
                                                    context)})
        respondo['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return respondo
    return render (request, 'e_mall/location_products.html', context)
@requires_csrf_token
@login_required
def delete_about(request, pk):
    post = get_object_or_404(Profile,pk=pk)
    if request.user == post.username:
        post.delete()
        u_id = post.username            
        return redirect('e_mall:user_catalog', u_id)        
    else:
        return HttpResponse('You are not authorized to delete this post')

@login_required
@require_http_methods(["DELETE"])
def delete_post(request, post_id):    
    try:
        post = Products.objects.get(id=post_id, seller=request.user)
        post.delete()
        return JsonResponse({'success': True})
    except Products.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
@requires_csrf_token    
@login_required
def edit_profile(request):   
    if request.method == 'POST':
        try:
            u_prof=Profile.objects.get(username=request.user)
            form = ProfileForm(request.POST, request.FILES, instance=u_prof)     #editing about for certain user       
            if form.is_valid():                
                u_id=request.user
                form.save()
                return redirect('e_mall:user_catalog', u_id)               
        except:
            form = ProfileForm(request.POST, request.FILES)     #creating about for user without one
            if form.is_valid():
                profile = form.save(commit=False)
                profile.username = request.user
                u_id=profile.username
                profile.save()
                return redirect('e_mall:user_catalog', u_id)
    else:        
        form = ProfileForm()
        try:
            user_about = Profile.objects.get(username=request.user)
            form = ProfileForm(instance=user_about)            
        except:
            user_about=None              
    return render (request, 'e_mall/user_profile.html', {'form':form})     
@requires_csrf_token
@login_required
def follow_user(request, seller_id):
    #simple code but META couldnt so had to come with own solution
    user_to_follow_id = User.objects.get(username=seller_id)
    user_to_followo = user_to_follow_id.id
    user_to_follow = User.objects.get(pk=user_to_followo)
    if request.user != user_to_follow:   
        if ProfileFollow.objects.filter(follower=request.user, followed=user_to_follow_id).exists():
            ProfileFollow.unfollow(request.user,user_to_follow)        
        else:
            ProfileFollow.follow(request.user,user_to_follow)
    else:
        request.session['lamessage']="you can't follow yourself"        
    return redirect('e_mall:user_catalog', seller_id)

def about_maita(request):
    e_categories_by_order, categories_by_order = navbar()
    aboutsignal='aboutsignal'
    context = {
        'aboutsignal':aboutsignal,     
        'categories':categories_by_order,
        'electronic_category':e_categories_by_order
    }
    return render(request, 'e_mall/about_maita.html', context)
    

       
    
        