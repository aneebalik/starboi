import imp
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from friend.models import FriendList, FriendRequest
from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus

from accounts.models import Account
from django.db.models import Q
# from accounts.forms import AccountUpdateForm




# Create your views here.





def account_view(request, *args, **kwargs):
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends
	
		# Define template variables
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # friend_request_status.FriendRequestStatus
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				# CASE1: Request has been sent from THEM to YOU
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass
			
		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "chat_account/account.html", context)

		
def account_search_view(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			print('skldfjasdfkjklasjdf')
			print(search_query)
			search_results = Account.objects.filter(Q(username__icontains=search_query))
			print(search_results)
			user = request.user
			accounts = [] # [(account1, True), (account2, False), ...]
			if user.is_authenticated:
				# get the authenticated users friend list
				try:
					auth_user_friend_list = FriendList.objects.get(user=user)
					for account in search_results:
						accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
					context['accounts'] = accounts

				except:
					pass
			else:
				for account in search_results:
					accounts.append((account, False))
				context['accounts'] = accounts
				
	return render(request, "chat_account/search.html", context)


# def edit_account_view(request, *args, **kwargs):
# 	if not request.user.is_authenticated:
# 		return redirect("login")
# 	user_id = kwargs.get("user_id")
# 	account = Account.objects.get(pk=user_id)
# 	if account.pk != request.user.pk:
# 		return HttpResponse("You cannot edit someone elses profile.")
# 	context = {}
# 	if request.POST:
# 		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
# 		if form.is_valid():
# 			form.save()
# 			new_username = form.cleaned_data['username']
# 			return redirect("account:view", user_id=account.pk)
# 		else:
# 			form = AccountUpdateForm(request.POST, instance=request.user,
# 				initial={
# 					"id": account.pk,
# 					"email": account.email, 
# 					"username": account.username,
# 					"profile_image": account.profile_image,
# 					"hide_email": account.hide_email,
# 				}
# 			)
# 			context['form'] = form
# 	else:
# 		form = AccountUpdateForm(
# 			initial={
# 					"id": account.pk,
# 					"email": account.email, 
# 					"username": account.username,
# 					"profile_image": account.profile_image,
# 					"hide_email": account.hide_email,
# 				}
# 			)
# 		context['form'] = form
# 	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
# 	return render(request, "chat_account/edit_account.html", context)
