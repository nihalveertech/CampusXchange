from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid


# -------------------------
# Validators
# -------------------------

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Enter a valid 10-digit phone number."
)


# -------------------------
# Category Choices
# -------------------------

CATEGORY_CHOICES = [
    ('textbooks', 'Textbooks & Notes'),
    ('electronics', 'Electronics'),
    ('smartphones', 'Smartphones'),
    ('engineering', 'Engineering Tools'),
    ('furniture', 'Study Furniture'),
    ('vehicles', 'Vehicles'),
    ('gadgets', 'Gadgets & Accessories'),
    ('printers', 'Printers & Xerox'),
    ('clocks', 'Alarm Clocks'),
    ('notes', 'Handwritten Notes'),
    ('other', 'Other'),
]

QUALITY_CHOICES = [
    ('like_new', 'Like New'),
    ('excellent', 'Excellent'),
    ('good', 'Good'),
    ('fair', 'Fair'),
    ('usable', 'Usable'),
]

LISTING_TYPE_CHOICES = [
    ('sell', 'Sell'),
    ('donate', 'Donate'),
    ('exchange', 'Exchange'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('sold', 'Sold'),
    ('inactive', 'Inactive'),
]
sold_at = models.DateTimeField(null=True, blank=True)


# -------------------------
# Profile Model
# -------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=10, blank=True, validators=[phone_validator])
    college = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# -------------------------
# Item Model
# -------------------------

class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='good')
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES, default='sell')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True)

    phone = models.CharField(max_length=10, validators=[phone_validator])
    show_phone = models.BooleanField(default=False)

    is_negotiable = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    wanted_items = models.TextField(blank=True)
    wanted_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    open_to_offers = models.BooleanField(default=True)

    image = models.ImageField(upload_to='items/', blank=True, null=True)

    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def get_category_display_with_emoji(self):
        emoji_map = {
            'textbooks': '📚',
            'electronics': '💻',
            'smartphones': '📱',
            'engineering': '🔧',
            'furniture': '🪑',
            'vehicles': '🏍️',
            'gadgets': '🎮',
            'printers': '🖨️',
            'clocks': '⏰',
            'notes': '📝',
            'other': '📦',
        }
        emoji = emoji_map.get(self.category, '')
        return f"{emoji} {self.get_category_display()}"


# -------------------------
# Item Images
# -------------------------

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.item.title}"


# -------------------------
# Wishlist
# -------------------------

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'item']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"


# -------------------------
# Transaction Model
# -------------------------

class Transaction(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    payment_method = models.CharField(max_length=50, default='Cash/UPI')

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['buyer']),
            models.Index(fields=['seller']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        if self.buyer == self.seller:
            raise ValidationError("Buyer and seller cannot be the same.")

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"CX-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.invoice_number}"


# -------------------------
# Messages
# -------------------------

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)

    content = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
        ]

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


# -------------------------
# Reports
# -------------------------

class Report(models.Model):

    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('fraud', 'Fraud/Scam'),
        ('inappropriate', 'Inappropriate Content'),
        ('duplicate', 'Duplicate Listing'),
        ('other', 'Other'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reports')

    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField()

    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_resolved']),
        ]

    def __str__(self):
        return f"{self.reason} - {self.item.title}"
