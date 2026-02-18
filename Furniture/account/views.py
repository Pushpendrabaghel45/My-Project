from django.shortcuts import render, redirect, get_object_or_404
from account.models import Product, Category
from django.core.cache import cache



# def admin_dashboard(request):
#     products = Product.objects.all()
#     return render(request, 'admin/dashboard.html', {'products': products})



def admin_categories(request):
    return render(request, 'admin/categories.html')

def admin_personal_details(request):
    return render(request, 'admin/personaldetails.html')

def admin_logout(request):
    print("chala inside route se")
    request.session['user_logged_in'] = False
    request.session.flush()  # clear session
    return redirect('admin_login')

def admin_dashboard(request):
    total_products = Product.objects.count()
    return render(request, 'admin/dashboard.html', {
        'total_products': total_products
    })


# def admin_products(request):
#     products = Product.objects.all()
#     return render(request, 'admin/products.html', {'products': products})

def admin_products(request):
    products = cache.get('all_products')
    if not products:
        products = Product.objects.all()
        cache.set('all_products', products, timeout=300)
    return render(request, 'admin/products.html', {
        'products': products
    })



def add_product(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id) 

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )

        return redirect('admin_products')

    return render(request, 'admin/product_add.html', {'categories': categories})


#Edit Product

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        # product.description = request.POST['description']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        return redirect('admin_products')

    return render(request, 'admin/product_form.html', {'product': product})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('admin_products')

# Add Product 

def admin_product_add(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            price=request.POST['price'],
            category_id=request.POST['category'],
            image=request.FILES['image']
        )
        return redirect('admin_products')

    return render(request, 'admin/product_add.html', {'categories': categories})



# CATEGORY LIST
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin/categories.html', {'categories': categories})


# ADD CATEGORY
def admin_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('admin_categories')

    return render(request, 'admin/category_add.html')


# EDIT CATEGORY
def admin_category_edit(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('admin_categories')

    return render(request, 'admin/category_edit.html', {'category': category})


# DELETE CATEGORY
def admin_category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('admin_categories')


