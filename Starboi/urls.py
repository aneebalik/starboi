from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from personal.views import (
	chat_home_screen
)
from chat_account.views import (
    account_search_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('home.urls')),
    path('store/', include('store.urls')),
    path('cart/',include('carts.urls')),
    path('accounts/',include('accounts.urls'),),
    path('blog/',include('blog.urls')),

    #chat urls
    path('personal/', chat_home_screen, name='chat_home_screen'),
    path('search/', account_search_view, name="search"),
    path('chat_account/',include('chat_account.urls',namespace='chat_account')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('friend/', include('friend.urls', namespace='friend')),

    #orders
    path('orders/',include('orders.urls')),
    path('adminpanel/',include('adminpanel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
