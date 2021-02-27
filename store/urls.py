from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #Leave as empty string for base url
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

	path('login/', views.login, name="login"),
	path('signup/', views.signup, name="signup"),
	path("logout/", views.logoutpage, name = "logout"),
	path('accountcreated/', views.accountcreated, name="accountcreated"),
	path('landing/', views.landing, name="landing"),
	path('clubshirts/', views.clubshirts, name="clubshirts"),
	path('technology/', views.technology, name="technology"),
	path('troy/', views.troy, name="troy"),
	path('dances/', views.dances, name="dances"),
	path('yearbooks/', views.yearbooks, name="yearbooks"),
	path('favorites/', views.favorites, name="favorites"),
	path('', views.home, name="home"),
	path('<int:pk>/', views.productdetail, name="productdetail"),
	path('product_like/<int:pk>/', views.product_like, name="product_like"),
	path('addcomment/', views.addcomment, name="addcomment"),
	path('resourcesused/', views.resourcesused, name="resourcesused"),
	path('description/', views.description, name="description"),

	#Forgot Password

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"), name="reset_password"),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"), name="password_reset_done"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"), name="password_reset_confirm"),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"), name="password_reset_complete"),


]
