from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password):
        if not email:
            raise ValueError("User email address can't be blank")
        if not username:
            raise ValueError("User Username can't be blank")
        
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, first_name, last_name, email, username, password):
        user=self.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            password = password
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff=True
        user.is_admin = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    #Mandatory fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    #Authentication 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    @property
    def get_role(self):
        if self.role == 1:
            user_role = "Vendor"
        elif self.role == 2:
            user_role = "Customer"
        else:
            user_role = "Admin"
        return user_role

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="users/profile_pictures", blank=True, null=True, default="users/default_pictures/default_food.jpg")
    cover_photo = models.ImageField(upload_to="users/cover_photos", blank=True, null=True, default="users/default_pictures/default-cover.png")
    address = models.CharField(max_length=250, blank=True, null=True)
    #address_line2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    lattitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def full_address(self):
        #return f"{self.address_line1}, {self.address_line2}"
        return f"{self.address}"
    def __str__(self):
        return self.user.email
