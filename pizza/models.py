from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
     def create_validator(self, request_POST):
          EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
          errors = {}
          if len(request_POST['first_name']) < 2:
               errors['first_name'] = "First name must be longer than 2 characters."
          if len(request_POST['last_name']) < 2:
               errors['last_name'] = "Last name must be longer than 2 characters."
          if len(request_POST['email']) < 8:
               errors['email'] = "email must be longer than 8 characters."
          if len(request_POST['password']) < 8:
               errors['password'] = "Password must be longer than 8 characters."
          if request_POST['password'] != request_POST['password_confirmation']:
               errors['password_confirmation'] = "Password confirmation does not match Password."
          if not EMAIL_REGEX.match(request_POST['email']):
               errors['regex'] = "email is not in correct format."
          return errors

class User(models.Model):
     first_name = models.CharField(max_length=45)
     last_name = models.CharField(max_length=45)
     email = models.CharField(max_length=45)
     address = models.CharField(max_length=100)
     password = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     objects = UserManager()
     def __str__(self):
          return f"{self.last_name}, {self.first_name}"

class Size(models.Model):
     name = models.CharField(max_length=60)
     price = models.DecimalField(max_digits=4, decimal_places=2)
     def __str__(self):
          return f"{self.name} for ${self.price}"

class Topping(models.Model):
     name = models.CharField(max_length=60, unique=True)
     def __str__(self):
          return self.name

class Pizza(models.Model):
     name = models.CharField(max_length=100, null=True, blank=True)
     created_by = models.ForeignKey(User, related_name='pizzas', on_delete=models.CASCADE, null=True)
     size = models.ForeignKey(Size, related_name='size_pizzas', on_delete=models.CASCADE, blank=True)
     toppings = models.ManyToManyField(Topping, related_name='toppings')
     def __str__(self):
          return f'{self.name}-{self.size.name} with {self.toppings.count()} toppings for {self.size.price} by {self.created_by}'


class Order(models.Model):
     order_user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True)
     order_timestamp = models.DateTimeField(auto_now_add=True)
     order_item = models.ManyToManyField(Pizza, related_name='ordered')
     order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)



# class Order(models.Model):
#      order_client = models.ForeignKey(User, on_delete=models.CASCADE)-----
#      order_timestamp = models.DateTimeField(auto_now_add=True)
#      order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

#      def __str__(self):
#           return f"Order number {self.id}"

