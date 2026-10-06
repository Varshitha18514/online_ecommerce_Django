from django.shortcuts import render,redirect
from django.http import HttpResponse
from userapp.models import User,Product,UserProfile,Order
import decimal

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        User.objects.create(username=username,email=email,phone=phone,password=password)
        return redirect("login_link")

    else:
        return render(request,"userapp/signup.html")

def login(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email = email,password=password).first()
        if(user):
            request.session["user_id"] = user.id
            request.session["user_name"] = user.username
            return redirect("dashboard_link")
        else:
            return HttpResponse("Invalid credentials")
    else:
        return render(request,"userapp/login.html")

    

def dashboard(request):
    products = Product.objects.all()
    return render(request,"userapp/dashboard.html",{"products":products})

def profileUpdate(request):
    if request.method == "POST":
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        state = request.POST.get("state")
        country = request.POST.get("country")
        address = request.POST.get("address")
        profile_pic = request.FILES.get("profile_pic")

        user_id = request.session.get("user_id")
        user = User.objects.get(id = user_id)

        profile = UserProfile.objects.get(user=user)
        profile.city=city
        profile.state=state
        profile.pincode=pincode
        profile.address=address
        profile.country=country

        if profile_pic: profile.profile_pic=profile_pic
        profile.save()
        return redirect("dashboard_link")
    else:
        return render(request,"userapp/profile_update.html")

def profile(request):
    user_id = request.session.get("user_id")
    user= UserProfile.objects.filter(id = user_id).first()
    return render(request,"userapp/profile.html",{"user":user})

def product_details(request,id):
    product = Product.objects.get(id=id)
    return render(request,"userapp/product_details.html",{"product":product})

def order(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        state = request.POST.get("state")
        address = request.POST.get("address")

        user_id =  request.session.get("user_id")
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=id)
        total = product.price*decimal.Decimal(quantity)

        Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            total=total,
            city=city,
            pincode=pincode,
            state=state,
            address=address
        )
        return redirect("dashboard_link")
    return render(request,"userapp/order.html")



