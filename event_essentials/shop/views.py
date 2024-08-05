from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Orders,OrderUpdate,signup, RentInfo,ThemeProduct
from math import ceil
from django.db.models import Q 
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
 



  # Adjust the import as per your actual model name

def LoginPage(request):
    if request.method == "POST":
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            if '@' in username_or_email:
                # Fetch user by email if '@' is in username_or_email
                user = signup.objects.get(email=username_or_email)
            else:
                # Otherwise, fetch user by username
                user = signup.objects.get(username=username_or_email)

            if user.passwd == password:
                request.session['username'] = user.username
                return redirect('/shop')  # Redirect to the shop page after successful login
            else:
                messages.error(request, 'Invalid password')  # Display error message for incorrect password
        except signup.DoesNotExist:
            messages.error(request, 'Invalid credentials')  # Display error message for invalid username/email

    return render(request, "shop/login.html")

def SignupPage(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_no = request.POST.get('phone_no')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
        else:
            signup.objects.create(firstname=firstname, lastname=lastname, username=username, email=email, passwd=password1, city=city, state=state, phone_no=phone_no)
            messages.success(request, 'Account created successfully')
            return redirect('login')
    
    return render(request, "shop/signup.html")




def index(request):
    # products= Product.objects.all()
    # print(products)   
    allProds = []
    catprods = Product.objects.values('category','product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n= len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
        
    params = {'allProds':allProds}
    return render(request,"shop/index.html", params)

def about(request):
    return render(request,'shop/about_us.html')

def contact(request):
    thank = False
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone_no=request.POST.get('phone_number','')
        desc = request.POST.get('desc','')
        print(name , email, phone_no, desc)
        contact = Contact(name=name, email=email, phone_no=phone_no, desc=desc)
        contact.save()
        thank = True
    return render(request,'shop/contact.html',{'thank':thank})

def rent(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        need_extra_info = request.POST.get('need_extra_info') == 'on'
        extra_info_text = request.POST.get('extra_info_text', '')

        # Create Rental object
        rental = RentInfo(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            need_extra_info=need_extra_info,
            extra_info_text=extra_info_text
        )
        rental.save()

        return HttpResponse("Form submitted successfully!")  # You can redirect to a success page instead

    return render(request, 'shop/rent.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.product_name.lower() or query in item.category.lower() :
        return True
    else:
        return False



def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}  
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}

    return render(request, 'shop/search.html', params)


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # Pass 'email' along with 'thank' and 'id'
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id, 'email': email})

    return render(request, 'shop/checkout.html')





def theme(request):
    allProds = []
    catprods = ThemeProduct.objects.values('theme_category').distinct()
    cats = [item['theme_category'] for item in catprods]
    for cat in cats:
        prod = ThemeProduct.objects.filter(theme_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "shop/theme.html", params)


def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('LoginPage') # Redirect to the shop page after logout

def payment(request):
    return render(request,'shop/payment.html')

def privacypolicy(request):
    return render(request,'shop/privacypolicy.html')



