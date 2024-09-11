from django.urls import path
from . import views

urlpatterns=[

path('',views.index,name='home'),
path('generate/text/',views.text,name='text'),
path('generate/email/',views.email,name='email'),
path('generate/url/',views.url,name='url'),
path('generate/location/',views.location,name='location'),
path('generate/whatsapp/',views.whatsapp,name='whatsapp'),
path('generate/vcard/',views.vcard,name='vcard'),
path('generate/wifi/',views.wifi,name='wifi'),
path('generate/call/',views.call,name='call'),
path('generate/terms-and-conditions/',views.terms_and_conditions,name='terms-and-conditions'),
 path('privacy-policy/', views.privacy_policy, name='privacy-policy'),

path('api/documentation/',views.api_documentation,name='api-docs'),
path('api/logo/format/', views.api_logoEncodingDecoding, name='logo-format'),
path('api/generate-qr/',views.api_generate_qr,name='api')
]