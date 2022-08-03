from django.urls import path

from chat_account.views import (
	account_view,
	# edit_account_view,
	# crop_image,
    account_search_view,
)

app_name = 'chat_account'

urlpatterns = [

	path('<int:user_id>/', account_view, name="view"),
	# path('<user_id>/edit/', edit_account_view, name="edit"),
	# path('<user_id>/edit/cropImage/', crop_image, name="crop_image"),


    path('search/',account_search_view,name='search'),

	
]