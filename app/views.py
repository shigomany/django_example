from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from app.models import *
from asgiref.sync import sync_to_async, async_to_sync
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Avg, Count, Sum

@sync_to_async
def auth(request):
    if request.method == 'POST':
        # NHJ9921gby-
        form = UserForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.errors['__all__'] = form.error_class(["User not found"])
                return render(request, 'auth.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'auth.html', {'form': form})

@sync_to_async
def logout(request):
    logout(request)
    return redirect('auth')

@sync_to_async
@login_required(login_url='auth/')
def index(request):
    books = Book.objects.select_related('author', 'publisher').all()
    
    cart = Cart.objects.annotate(
        books_count=Count('books')
    ).filter(user__pk__exact=request.user.pk).first()
    return render(request, 'index.html', context={'books': books, 'cart_count': cart.books_count if cart else 0})

@sync_to_async
@require_POST
@login_required(login_url='auth/')
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    curren_cart = Cart.objects.filter(user__pk__exact=request.user.pk).first()
    if not curren_cart:
        new_cart = Cart(user=request.user)
        new_cart.save()
        new_cart.books.add(book)
        new_cart.save()
    else:
        cart_book = CartBook(cart=curren_cart, book=book)
        cart_book.save()
    return redirect('index')

@sync_to_async
@require_GET
@login_required(login_url='auth/')
def cart(request):
    # book = get_object_or_404(Book, pk=pk)
    cart = Cart.objects.annotate(
        books_count=Count('books')
    ).prefetch_related('books').filter(user__pk__exact=request.user.pk).first()

    cart_books = CartBook.objects.filter(cart=cart.pk).select_related('book').all() if cart else None
    
    order_sum = sum([el.price_d for el in cart.books.all()]) if cart else None
    return render(request, 'cart.html', context={
        'cart_books': cart_books, 
        'cart_count': cart.books_count if cart else 0,
        'order_price': order_sum,
    })

@sync_to_async
@require_POST
@login_required(login_url='auth/')
def cart_delete(request, pk):
    cart_book = CartBook.objects.filter(pk__exact=pk).delete()
    return redirect('cart-detail')