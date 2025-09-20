from django.shortcuts import render, redirect 
from django.contrib.auth.models import User, auth
from e_mall.forms.usersignup import MyCustomSignupForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@requires_csrf_token  
def signup(request):
    try:
        if request.method == 'POST':
            form= MyCustomSignupForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                password=form.cleaned_data['password1']
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect('e_mall:login')                         
        else:
            form= MyCustomSignupForm()
        return render(request, 'e_mall/signup.html', {'form':form})
    except:
        return redirect('e_mall:signup')
    
class CustomLoginView(LoginView):
    template_name = 'e_mall/login.html'  
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

@csrf_protect
@requires_csrf_token 
def logout(request):
    auth.logout(request)
    return redirect('e_mall:store')