# views.py: Django Views Definition
# --------------------------------
# In Django, the views.py file contains "view" functions or classes
# that take a web request and return a web response. They:
# 1. Get data from models (the database).
# 2. Process business logic (filter, count, create records).
# 3. Render HTML templates with context data.
# Think of views as the "brain" of each web page: they decide what data to show
# and which template to use.
# 
# Analogy for a 5-year-old:
# "Imagine a restaurant. The view is like the waiter:
#  - You (the browser) tell the waiter (view) what you want (URL request).
#  - The waiter goes to the kitchen (database/models) to get your food (data).
#  - Then the waiter brings the food on a plate (HTML template) back to you.
# That is how a Django view works!"

from django.shortcuts import render  # Renders HTML templates with context
from datetime import date, timedelta  # For date calculations
from django.db.models import Count   # To perform aggregation queries
from .models import Customer, Interaction  # Import our data models

# Home page: list all customers
def index(request):
    # Query all Customer records
    customers = Customer.objects.all()
    # Prepare context dict for template
    context = {"customers": customers}
    # Render index.html, passing the customer list
    return render(request, "index.html", context=context)

# Create Customer view: handles form submission
def create_customer(request):
    # Only process POST requests with form data
    if request.method == "POST":
        # Extract form fields from request
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        social_media = request.POST["social_media"]
        # Create and save a new Customer record
        customer = Customer.objects.create(
            name=name, email=email, phone=phone, address=address, social_media=social_media
        )
        customer.save()
        # Feedback message for the user
        msg = "Successfully Saved a Customer"
        # Render add.html with success message
        return render(request, "add.html", context={"msg": msg})
    # If not POST, just render empty form
    return render(request, "add.html")

# Summary view: show interactions in last 30 days
def summary(request):
    # Calculate date 30 days ago
    thirty_days_ago = date.today() - timedelta(days=30)
    # Filter Interaction records from last 30 days
    interactions = Interaction.objects.filter(
        interaction_date__gte=thirty_days_ago
    )
    # Total count of interactions
    count = len(interactions)
    # Aggregate by channel and direction, counting each group
    interactions = (
        interactions
        .values("channel", "direction")
        .annotate(count=Count('channel'))
    )
    # Context for template
    context = {
        "interactions": interactions,
        "count": count
    }
    # Render summary.html with aggregated data
    return render(request, "summary.html", context=context)

# Interact view: record a customer interaction
def interact(request, cid):
    # Get choice lists from model class constants
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    # Base context for GET or POST
    context = {"channels": channels, "directions": directions}

    # Handle form submission
    if request.method == "POST":
        # Look up the Customer by ID
        customer = Customer.objects.get(id=cid)
        # Read selected values from POST
        channel = request.POST["channel"]
        direction = request.POST["direction"]
        summary_text = request.POST["summary"]
        # Create and save new Interaction record
        interaction = Interaction.objects.create(
            customer=customer,
            channel=channel,
            direction=direction,
            summary=summary_text
        )
        interaction.save()
        # Add success message to context
        context["msg"] = "Interaction Success"
        # Render the form again with message
        return render(request, "interact.html", context=context)

    # For GET requests, just render the form
    return render(request, "interact.html", context=context)
