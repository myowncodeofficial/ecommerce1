from django.shortcuts import render, get_object_or_404
from .models import Category,Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# Create your views here.

def front(request):
    return render(request,'front.html')

def allProdCat(request,c_slug=None):
    c_page = None
    products_list = None
    if c_slug!=None:
        c_page = get_object_or_404(Category,slug=c_slug)
        products_list = Product.objects.all().filter(category=c_page,available=True)
    else:
        products_list = Product.objects.all().filter(available=True)
    paginator = Paginator(products_list,6)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage,InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request,'category.html',{'category':c_page,'products':products})
def prodDetail(request,c_slug,product_slug):
    try:
        product=Product.objects.get(category__slug=c_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})


def register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        firstname = request.POST['first_name']
        secondname = request.POST['last_name']
        email = request.POST['email']
        pwrd = request.POST['password']
        cpwrd = request.POST['cpassword']
        if pwrd == cpwrd:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
                return redirect('shop:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exist')
                return redirect('shop:register')
            else:
                user = User.objects.create_user(username=username, first_name=firstname, last_name=secondname,
                                                email=email,
                                                password=pwrd)
                user.save()
                messages.info(request, 'registered successfully')
                return redirect('shop:login')
        else:
            messages.info(request,'Password is not matching')
            return redirect('shop:register')
        return redirect('shop:login')
    return render(request, template_name='register.html')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('shop:allProdCat')
        else:
            messages.info(request, 'Invalid credential')
            return redirect('shop:login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
