from django.urls import path, re_path
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemap import ArticleSitemap, StaticViewSitemap

sitemaps = {
	'articles': ArticleSitemap,
	'static': StaticViewSitemap
}

urlpatterns = [
  	path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
	path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
     name='sitemap'),
	path('', views.blank, name='index'),
	path('services/', views.services, name='services'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('contact/', views.contact, name='contact'),
	path('thanks/', views.contactThanks, name="thanks"),
	path('contact-error/', views.contactError, name="contact-error"),
	path('register/', views.register, name="register"),
	path('quote/', views.requestQuote, name='quote'),
	path('knowledge/', views.school, name='school'),
	path('knowledge/<slug:slug>/', views.article, name='article'),
	path('about/', views.about, name='about'),
	path('faq/', views.faq, name='faq'),
	path('<int:status_code>/', views.errorPage, name='error'),
	path('me/', views.currentUserProfile, name='profile'),
	path('register-error/', views.registerError, name='register-error'),
]