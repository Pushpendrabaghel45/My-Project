from django.db import models


# CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




# Product

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)   
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


 


# Home page models

# 🔹 HERO SECTION
class HomeHero(models.Model):
    tag = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='home/hero/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Hero Section"


# 🔹 COUNTERS
class HomeCounter(models.Model):
    title = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.title


# 🔹 CATEGORIES
class HomeCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='home/categories/')
    item_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# 🔹 PRODUCTS
class HomeProduct(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='home/products/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# 🔹 BANNER
class HomeBanner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='home/banner/')
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# 🔹 TESTIMONIAL
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
