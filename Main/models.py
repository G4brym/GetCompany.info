from django.db import models
from django.contrib.auth.models import User

class Visits(models.Model):
    usersVisits = models.IntegerField(default=0)
    botsVisits = models.IntegerField(default=0)
    date = models.TextField()

    class Meta:
        app_label = 'Main'

class Companies(models.Model):
    identifier = models.TextField(max_length=100, unique=True)
    name = models.TextField(max_length=100)

    cae = models.TextField(max_length=100, null=True)
    state = models.TextField(max_length=100, null=True)
    city = models.TextField(max_length=100, null=True)
    # when the company started activities
    started_at = models.TextField(max_length=100, null=True)
    address = models.TextField(max_length=500, null=True)
    address_l2 = models.TextField(max_length=500, null=True)
    phone = models.TextField(max_length=100, null=True)
    mobile = models.TextField(max_length=100, null=True)
    fax = models.TextField(max_length=100, null=True)
    email = models.TextField(max_length=100, null=True)

    info = models.BooleanField(default=False)
    about = models.TextField(max_length=10000, null=True)
    products = models.TextField(max_length=10000, null=True)
    brands = models.TextField(max_length=5000, null=True)
    tags = models.TextField(max_length=10000, null=True)

    links = models.BooleanField(default=False)
    website = models.TextField(max_length=100, null=True)
    facebook = models.TextField(max_length=100, null=True)
    twitter = models.TextField(max_length=100, null=True)
    linkedin = models.TextField(max_length=100, null=True)
    googleplus = models.TextField(max_length=100, null=True)

    active = models.BooleanField(default=True)

    # 1-> about
    # 2-> products
    # 3-> brands
    # 4-> tags
    active_tab = models.IntegerField(default=1)
    already_crawled = models.BooleanField(default=False)
    error_crawling = models.BooleanField(default=False)

    visits_users = models.IntegerField(default=0)
    visits_bots = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        app_label = 'Main'

class Tokens(models.Model):
    id = models.TextField(max_length=32, primary_key=True)
    company = models.ForeignKey(Companies)
    user = models.ForeignKey(User, null=True)

    valid = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        app_label = 'Main'

class CAE(models.Model):
    id = models.TextField(max_length=10, primary_key=True)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        app_label = 'Main'