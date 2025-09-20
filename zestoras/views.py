from django.shortcuts import render

# Create your views here.



def home(request):
    return render(request, 'home.html') 
def hometest(request):
    return render(request, 'hometest.html') 

def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')

def recipe_view(request):
    return render(request, 'homeper.html')