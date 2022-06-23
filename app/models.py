import imp
from django.db import models
from django.contrib.auth.models import AbstractUser
from app.managers import CustomUserManager
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator


# Категория товара
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'Category(name={self.name})'

# Издалельство
class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'Publisher(name={self.name})'

# Автор книги
class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url_avatar = models.CharField(max_length=2049, validators=[URLValidator()], null=True, blank=True)

    def __str__(self) -> str:
        return f'Author(name={self.name})'

# Книга
class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    description = models.TextField(max_length=10000)
    quantity = models.PositiveIntegerField()
    url_image = models.CharField(max_length=2048, validators=[URLValidator()])

    categories = models.ManyToManyField(Category, related_name='cats', blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'Book(title={self.title}, price={self.title}, sale={self.sale})'

    @property
    def price_d(self):
        return self.price * (100 - (self.sale if self.sale else 0)) / 100

# Кастомный пользователь
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    favorite_items = models.ManyToManyField(Book, related_name='favorites')

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'CustomUser(email={self.email})'


# Корзина
class Cart(models.Model):
    books = models.ManyToManyField(Book, through='CartBook')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class CartBook(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)









