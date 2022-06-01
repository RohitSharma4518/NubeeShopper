from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from math import ceil
import json
from NubeeShopperApp.models import Product, Orders, OrderUpdate, Contact
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import razorpay
# Create your views here.


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.product_description.lower() or query in item.product_name.lower() or query in item.product_category.lower():
        return True
    else:
        return False


def home(request):
    allProds = []
    catprods = Product.objects.values('product_category', 'id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'NubeeShopperApp/index.html', params)


def signin(request):
    if request.method == "POST":
        user_name_login = request.POST.get('username')
        password_login = request.POST.get('password')
        user = authenticate(username=user_name_login, password=password_login)

        if user is not None:
            print("if is accessed")
            login(request, user)
            username_template = user.username
            # messages.success(request, "Your account has been successfully created!")
            # return redirect('home')
            allProds = []
            catprods = Product.objects.values('product_category', 'id')
            cats = {item['product_category'] for item in catprods}
            for cat in cats:
                prod = Product.objects.filter(product_category=cat)
                n = len(prod)
                nSlides = n // 4 + ceil((n / 4) - (n // 4))
                allProds.append([prod, range(1, nSlides), nSlides])
            params = {'allProds': allProds, 'username_html': username_template}
            return render(request, 'NubeeShopperApp/index.html', params)

        else:
            print("Else is called")
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    return render(request, 'NubeeShopperApp/signin.html')


def signup(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        e_mail = request.POST.get('email')
        pass_word = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')

        myuser = User.objects.create_user(user_name, e_mail, pass_word)
        myuser.save()

        messages.success(
            request, "Your account has been successfully created!")

        return redirect('signin')

    return render(request, 'NubeeShopperApp/signup.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def about(request):
    return render(request, 'NubeeShopperApp/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'NubeeShopperApp/contact.html')


def productview(request, myid):
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'NubeeShopperApp/productview.html', {'product': product[0]})


def producttracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(
                        {"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'NubeeShopperApp/producttracker.html')


def productsearch(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('product_category', 'id')
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(product_category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'NubeeShopperApp/productsearch.html', params)


def productpayment(request):
    return render(request, 'NubeeShopperApp/productpayment.html')


def productcheckout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'NubeeShopperApp/productcheckout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after the payment of user
        client = razorpay.Client(
            auth=("rzp_test_Qo0RJbccMXyZva", "M7MqN5i0xOr1AqEN69lvfwUL"))

        DATA = {
            "amount": int(order.amount)*100,
            "currency": "INR",
            # "receipt": "receipt#1",
            # "notes": {
            #     "key1": "value3",
            #     "key2": "value2"
            # }
        }
        client.order.create(data=DATA)

        return render(request, 'NubeeShopperApp/razor_pay.html', {'param_dict': DATA})

    return render(request, 'NubeeShopperApp/productcheckout.html')


@csrf_exempt
def paymentstatus(request):
    return render(request, 'NubeeShopperApp/paymentstatus.html')
