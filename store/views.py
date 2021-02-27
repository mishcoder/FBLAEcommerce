from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	# added code for sizes

	if action == 'small':
		orderItem.size = "small"
	elif action == 'medium':
		orderItem.size = "medium"
	elif action == 'large':
		orderItem.size = "large"

	# end 

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def signup(request):
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			email = form.cleaned_data.get('email')
			customer, created = Customer.objects.get_or_create(
			email=email,
			)
			customer.user = user
			customer.name = form.cleaned_data.get('first_name')
			customer.save()
			return redirect('/accountcreated')

		else:
			password1 = form.cleaned_data.get('password1')
			password2 = form.cleaned_data.get('password2')
			# username validation is not working
			# password validation (checking if the passwords are the same is not working either)
			#if User.objects.filter(username=username).exists():
				#messages.info(request, 'Username is already taken.')
			if password1 != password2:
				messages.info(request, 'Your passwords do not match')
			if len(password1) < 8:
				messages.info(request, 'Password must be at least 8 characters long.')
			if not re.findall('\d', password1):
				messages.info(request, 'Password must contain one numeric value.')
			if not re.findall('[a-z]', password1):
				messages.info(request, 'Password must contain at least one lowercase value.')
			if not re.findall('[A-Z]', password1):
				messages.info(request, 'Password must contain at least one uppercase value.')
			if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password1):
				messages.info(request, 'Password must contain at least one symbol.')
			if password1.isdigit():
				messages.info(request, 'The password may not be entirely numeric.')


	form = CreateUserForm
	return render(request, 'store/signup.html', context={"form":form})

def addcomment(request):
	#model = Comment
	#template_name = 'addcomment.html'
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()

	form = CommentForm
	return render(request, 'store/addcomment.html', context={"form": form})

def login(request):
		#issue = user has no customer, to fix: when person creates account and becomes user
		#also must become customer
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				auth.login(request, user)
				return redirect("/store")

			else:
				messages.info(request, 'Username or Password is incorrect.')

		context = {}
		return render(request, "store/login.html", context)

def landing(request):
	return render(request, 'store/landing.html')

def home(request):
	return render(request, 'store/home.html')

def logoutpage(request):
	logout(request)
	return redirect("/login")

def productdetail(request,pk):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	product = Product.objects.get(id = pk)
	if request.method == "POST":
		form = CommentForm(request.POST)

		if form.is_valid():
			newcomment = form.save(commit=False)
			newcomment.product = product
			newcomment.save()

	form = CommentForm

	model = Product
	    # template_name = MainApp/BlogPost_detail.html
	    # context_object_name = 'object'

	def get_context_data(self, **kwargs):
	    data = super().get_context_data(**kwargs)

	    likes_connected = get_object_or_404(Product, id=self.kwargs['pk'])
	    liked = False
	    if likes_connected.likes.filter(id=self.request.user.id).exists():
	        liked = True
	    data['number_of_likes'] = likes_connected.number_of_likes()
	    data['post_is_liked'] = liked
	    return data
	
	


	return render(request, 'store/testproduct.html', {'product': product, 'cartItems':cartItems,'form': form,})

def clubshirts(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/clubshirts.html', context)

def technology(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/technology.html', context)

def troy(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/troy.html', context)

def dances(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/dances.html', context)

def yearbooks(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/yearbooks.html', context)

def product_like(request, pk):
	product = get_object_or_404(Product, id=request.POST.get('product_id'))
	liked = False
	if product.likes.filter(id=request.user.id).exists():
		product.likes.remove(request.user)
		liked = False
	else:
		product.likes.add(request.user)
		liked = True

	return HttpResponseRedirect(reverse('productdetail',args=[str(pk)]))

def favorites(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	user = User.objects.get(id=request.user.id)
	favorites = user.product_likes.all()

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems, 'favorites': favorites}

	return render(request, 'store/favorites.html', context)




def accountcreated(request):
	return render(request, 'store/accountcreated.html')

def resourcesused(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}

	return render(request, 'store/resourcesused.html', context)

def description(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}

	return render(request, 'store/description.html', context)