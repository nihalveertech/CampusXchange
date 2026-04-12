from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.db import transaction
from .models import Item, Profile, Wishlist, Transaction, ItemImage, Message, Report
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
def home(request):
    featured_items = Item.objects.filter(status='active').order_by('-is_featured', '-created_at')[:6]
    return render(request, 'index.html', {'featured_items': featured_items})


def buy(request):
    items = Item.objects.all()

    query = request.GET.get('q', '').strip()
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    category = request.GET.get('category', '')
    if category:
        items = items.filter(category=category)

    location = request.GET.get('location', '')
    if location:
        items = items.filter(location__icontains=location)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        try:
            items = items.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            items = items.filter(price__lte=float(max_price))
        except ValueError:
            pass

    quality = request.GET.getlist('quality')
    if quality:
        items = items.filter(quality__in=quality)

    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'price_low':
        items = items.order_by('price')
    elif sort_by == 'price_high':
        items = items.order_by('-price')
    else:
        items = items.order_by('-created_at')

    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    items = paginator.get_page(page)

    return render(request, 'buy.html', {
        'items': items,
        'selected_category': category,
        'query': query,
    })
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def sell(request):
    if request.method == 'POST':
        item = Item.objects.create(
            seller=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            price=request.POST.get('price') or 0,
            quality=request.POST.get('quality'),
            listing_type='sell',
            location=request.POST.get('location'),
            address=request.POST.get('address', ''),
            phone=request.POST.get('phone'),
            show_phone=request.POST.get('show_phone') == 'on',
            is_negotiable=request.POST.get('is_negotiable') == 'on',
            status='active'
        )

        images = request.FILES.getlist('images')

        if images:
            item.image = images[0]
            item.save()

            for image in images[1:]:
                ItemImage.objects.create(item=item, image=image)

        messages.success(request, 'Your item has been listed successfully!')
        return redirect('item_detail', item_id=item.id)

    return render(request, 'sell.html')

@login_required
def donate(request):
    if request.method == 'POST':
        item = Item(
            seller=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            price=0,
            quality=request.POST.get('quality'),
            listing_type='donate',
            location=request.POST.get('location'),
            phone=request.POST.get('phone'),
        )

        images = request.FILES.getlist('images')
        if images:
            item.image = images[0]

        item.save()
        messages.success(request, 'Thank you for your donation! Your item has been listed.')
        return redirect('item_detail', item_id=item.id)

    return render(request, 'donate.html')


@login_required
def exchange(request):
    if request.method == 'POST':
        item = Item(
            seller=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            price=request.POST.get('price') or 0,
            quality=request.POST.get('quality'),
            listing_type='exchange',
            location=request.POST.get('location'),
            phone=request.POST.get('phone'),
            wanted_items=request.POST.get('wanted_items', ''),
            wanted_category=request.POST.get('wanted_category', ''),
            open_to_offers=request.POST.get('open_to_offers') == 'on',
        )

        images = request.FILES.getlist('images')
        if images:
            item.image = images[0]

        item.save()
        messages.success(request, 'Your exchange listing has been posted!')
        return redirect('item_detail', item_id=item.id)

    return render(request, 'exchange.html')


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Safe view increment
    Item.objects.filter(id=item.id).update(views=F('views') + 1)

    return render(request, 'item_detail.html', {'item': item})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller=request.user)

    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.category = request.POST.get('category')
        item.price = request.POST.get('price') or 0
        item.quality = request.POST.get('quality')
        item.location = request.POST.get('location')
        item.phone = request.POST.get('phone')
        item.is_negotiable = request.POST.get('is_negotiable') == 'on'

        images = request.FILES.getlist('images')
        if images:
            item.image = images[0]

        item.save()
        messages.success(request, 'Item updated successfully!')
        return redirect('item_detail', item_id=item.id)

    return render(request, 'sell.html', {'item': item, 'edit_mode': True})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller=request.user)

    # Soft delete instead of hard delete
    item.status = 'inactive'
    item.save()

    messages.success(request, 'Item removed successfully!')
    return redirect('dashboard')


@login_required
def dashboard(request):
    user_listings = Item.objects.filter(seller=request.user)
    user_purchases = Transaction.objects.filter(buyer=request.user).select_related('item', 'seller')
    user_wishlist = Wishlist.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'user_listings': user_listings,
        'user_listings_count': user_listings.filter(status='active').count(),
        'sold_count': user_listings.filter(status='sold').count(),
        'purchases_count': user_purchases.count(),
        'wishlist_count': user_wishlist.count(),
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        college = request.POST.get('college')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('register')

        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        Profile.objects.create(user=user, phone=phone, college=college)

        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('dashboard')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('dashboard')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully!')
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def toggle_wishlist(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, item=item)

    if not created:
        wishlist.delete()
        return JsonResponse({'status': 'removed'})

    return JsonResponse({'status': 'added'})


@login_required
def create_transaction(request, item_id):
    item = get_object_or_404(Item, id=item_id, status='active')

    if item.seller == request.user:
        messages.error(request, "You cannot buy your own item.")
        return redirect('item_detail', item_id=item.id)

    if request.method == 'POST':
        with transaction.atomic():
            item.refresh_from_db()
            if item.status != 'active':
                messages.error(request, "Item already sold.")
                return redirect('item_detail', item_id=item.id)

            Transaction.objects.create(
                buyer=request.user,
                seller=item.seller,
                item=item,
                amount=item.price or 0
            )

            from django.utils import timezone

            item.status = 'sold'
            item.save()

        messages.success(request, 'Purchase successful!')
        return redirect('item_detail', item_id=item.id)

    return redirect('item_detail', item_id=item.id)


def search(request):
    query = request.GET.get('q', '').strip()

    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    items = Item.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query),
        status='active'
    )[:10]

    results = [
        {
            'id': item.id,
            'title': item.title,
            'price': str(item.price) if item.price else 'Free',
            'image': item.image.url if item.image else None,
        }
        for item in items
    ]

    return JsonResponse({'results': results})
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = request.POST.get('phone', '')
        profile.college = request.POST.get('college', '')
        profile.save()

        messages.success(request, 'Profile updated successfully!')

    return redirect('dashboard')
def password_reset(request):
    return render(request, 'password_reset.html')
