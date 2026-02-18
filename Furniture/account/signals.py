from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Product, Category
from decimal import Decimal, InvalidOperation

@receiver(post_save, sender=Product)
def product_created_or_updated(sender, instance, created, **kwargs):
    if created:
        print(f"Product created: ")
    else:
        print(f"Product updated: ")
        
@receiver(pre_save, sender=Product)
def product_price_validation(sender, instance, **kwargs):
    try:
        price = Decimal(instance.price)
    except (InvalidOperation, TypeError):
        raise ValueError("Invalid price value")

    # if price < 0:
        raise ValueError("Product price cannot be negative")
    # price = instance.price
    # print("sender")
    # print(sender)
    # print("instance")
    # print(instance)
    # print("kwargs")
    # print(kwargs)
    if price<0:
        raise ValueError("Product price cannot be negative")


@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    print(f" Product deleted: {instance.name}")
    
@receiver(post_save, sender=Category)
def category_created(sender, instance, created, **kwargs):
    if created:
        print(f"Category created: {instance.name}")


@receiver(post_delete, sender=Category)
def category_deleted(sender, instance, **kwargs):
    print(f"Category deleted: {instance.name}")