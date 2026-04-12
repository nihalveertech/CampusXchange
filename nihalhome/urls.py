from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('donate/', views.donate, name='donate'),
    path('exchange/', views.exchange, name='exchange'),
    # Item pages
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),

    # User pages
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('password/change/', views.change_password, name='change_password'),
    path('password/reset/', views.password_reset, name='password_reset'),

    # API endpoints
    path('api/wishlist/<int:item_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('api/purchase/<int:item_id>/', views.create_transaction, name='create_transaction'),
    path('api/search/', views.search, name='search'),
]
