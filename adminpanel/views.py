from django.shortcuts import render,redirect
from django.template.defaultfilters import slugify
from django.contrib import messages

from accounts.models import Account
from category.models import Category
from store.models import Product, Variation
#store imports
from store.forms import ProductForm,VariationForm
from category.forms import CategoryForm
#cart imports
from carts.models import Cart,CartItem
from orders.models import Order,OrderProduct,Payment
from django.contrib.auth.decorators import login_required 
from django.db.models import Sum,Count

# Create your views here.

def admin_dashboard(request):



    return render(request,'adminpanel/admin_dashboard.html')


@login_required(login_url="login")
def admin_dashboard(request):
    if request.user.is_superadmin:
        total_revenue = round( Order.objects.filter(is_ordered = True).aggregate(sum = Sum('order_total'))['sum'])

        total_cost= round((total_revenue * .80))
        total_profit = round(total_revenue - total_cost)  
        
        product_count = OrderProduct.objects.all().count()
       
        context = {
            'total_revenue' : total_revenue,
            'total_cost' : total_cost,
            'total_profit' : total_profit,
            'product_count' : product_count,
        }
        return render (request,'adminpanel/admin_dashboard.html',context)
    else:
        return redirect('home')






def accounts_table(request,id):
    active_users = Account.objects.filter(is_admin=False, is_active=True)
    banned_users = Account.objects.filter(is_admin=False, is_active=False)

    context = {
        'active_users':active_users,
        'banned_users':banned_users,
    }
    if id == 1:
        return render(request,'adminpanel/accounts/active_user_account_table.html',context)
    else:
        return render(request,'adminpanel/accounts/banned_user_account_table.html',context)


#functions in account table(ban&unban)
def ban_user(request,id):
    user = Account.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('accounts',id=1)

def unban_user(request,id):
    user = Account.objects.get(id=id)
    user.is_active = True
    user.save()   
    return redirect('accounts',id=2)

def cart_table(request,id):
    carts = Cart.objects.all()
    cart_items = CartItem.objects.all().filter(is_active=True)
    context = {
        'carts' : carts,
        'cart_items' : cart_items,
    }
    
    if id==1:
        return render(request,'adminpanel/cart_table/cart.html',context)
    else:
        return render(request,'adminpanel/cart_table/cart_item.html',context)


def category_table(request,id):
    category      = Category.objects.all()

    context = {
        'category':category,
    }
    return render(request, 'adminpanel/category_table/category.html',context)
  
#category_table functions(add====dlt=======edit)
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            category_name = form.cleaned_data['category_name']
            slug          = slugify(category_name)
            category.slug = slug
            category.save()
            messages.success(request,'New Category added successfully')
            return redirect('category_table', id=1)
    context = {
        'form':form,
    }
    return render(request, 'adminpanel/category_table/add_category.html',context)

def edit_category(request,id):
    category = Category.objects.get(id=id)
    print(category)
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            slug          = slugify(category_name)
            category = form.save()
            category.slug = slug
            category.save()
            messages.success(request, 'Category edited succesfully')
            return redirect('category_table')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
    }
    return render(request,'adminpanel/category_table/add_category.html',context)

def delete_category(request):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category_table')



@login_required(login_url="login")
def order_table(request,id):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered=True,status='New')
        accepted_orders = Order.objects.filter(is_ordered=True,status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True,status="Completed")
        cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled")
        order_products = OrderProduct.objects.all()

        payments = Payment.objects.all()
        context = {
            'orders' : orders,
            'order_products' : order_products,
            'payments' : payments,
            'accepted_orders' : accepted_orders,
            'completed_orders' : completed_orders,
            'cancelled_orders' : cancelled_orders,
        }

        if id==1:
            return render (request,'adminpanel/order_table/new_orders.html',context)
        elif id==2:
            return render(request,'adminpanel/order_table/accepted_orders.html',context)
        elif id==3:
            return render(request,'adminpanel/order_table/completed_orders.html',context)
        elif id==4:
            return render(request,'adminpanel/order_table/cancelled_orders.html',context)
        elif id==5:
            return render(request,'adminpanel/order_table/order_products.html',context)
        else:
            return render(request,'adminpanel/order_table/payments.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_accepted(request,order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('order_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def order_completed(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Completed'
        order.save()
        return redirect('order_table',id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_cancelled(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('order_table',id=1 )
    else:
        return render(request,'adminpanel/order_table/order_cancelled.html')


#store

@login_required(login_url="login")
def store_table(request,id):
    if request.user.is_superadmin:
        products = Product.objects.all()
        variations =Variation.objects.all()

        context = {
            'products' : products,
            'variations' : variations,
        }
        if id==1:
            return render(request,'adminpanel/store_table/products.html',context)
        else:
            return render(request,'adminpanel/store_table/variations.html',context)
    else:
        return redirect('home')


def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            product = form.save(commit=False)
            product_name = form.cleaned_data['product_name']
            slug = slugify(product_name)
            product.slug = slug

            product.save()
            return redirect('store_table',id=1)
    else:
        form = ProductForm()
    context = {
        'form' : form,
    }
    return render(request,'adminpanel/store_table/add_product.html',context)

def edit_product(request,id):
    product = Product.objects.get(id=id)
    if request.method =='POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            slug = slugify(product_name)
            product = form.save()
            product.product_slug = slug
            product.save()
            return redirect('store_table',id=1)
    else:
        form = ProductForm(instance=product)
    context = {
        'form' : form,
    }
    return render (request,'adminpanel/store_table/add_product.html',context)

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('store_table',id=1)


@login_required(login_url="login")     
def add_variations(request):
    if request.user.is_superadmin:
        form = VariationForm()
        if request.method == 'POST':
            form = VariationForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_variations(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        if request.method =='POST':
            form = VariationForm(request.POST,instance=variation)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm(instance=variation)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def delete_variatons(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        variation.delete()
        return redirect('store_table',id=2)
    else:
        return redirect ('home')
