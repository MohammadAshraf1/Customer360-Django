# Import Django's model classes so we can define our own database models
from django.db import models

# This class represents the structure of a "Customer" table in the database
class Customer(models.Model):
    # Each customer will have an auto-generated ID as the primary key
    id = models.AutoField(primary_key=True)

    # The customer's name - stored as a string with a maximum of 100 characters
    name = models.CharField(max_length=100)

    # The customer's email - Django will validate that it's a real email format
    email = models.EmailField(max_length=100)

    # Phone number - stored as a string of up to 20 characters
    phone = models.CharField(max_length=20)

    # Address - stored as a string of up to 200 characters
    address = models.CharField(max_length=200)

    social_media = models.CharField(max_length=100, blank=True)

    # This is what will be shown when we print the object (e.g., in admin panel)
    def __str__(self):
        return str(self.id)

# This class represents the structure of an "Interaction" table in the database
class Interaction(models.Model):
    # Options for how the interaction was made (phone, SMS, etc.)
    CHANNEL_CHOICES = [
        ('phone', 'Phone'),
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('letter', 'Letter'),
        ('social_media', 'Social Media')
    ]

    # Whether the interaction was inbound or outbound
    DIRECTION_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ]

    # ForeignKey links each interaction to a specific customer
    # If the customer is deleted, their interactions will be deleted too (CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # The channel used (must be one of the choices)
    channel = models.CharField(max_length=15, choices=CHANNEL_CHOICES)

    # The direction of the interaction (must be one of the choices)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)

    # The date of the interaction is set automatically when it's created
    interaction_date = models.DateField(auto_now_add=True)

    # A short summary of the interaction
    summary = models.TextField()

# Exactly! ✅
#
# In Django:
#
# > Each class you define in models.py *is* a model.
#
# And each model:
# - becomes a **table** in the database.
# - has **attributes** (fields) that become **columns** in that table.
# - can be connected to other models (tables) using relationships like ForeignKey.
#
# ---
#
# 🔍 Example:
#
# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#
# This says:
# - "I want a **Customer table**."
# - "It should have a **name column**."
#
# class Interaction(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#
# This says:
# - "I want an **Interaction table**."
# - "It should have a **column linking to a specific Customer**."
#
# ---
#
# So yes — each class = **one model** = **one table** 📋.
