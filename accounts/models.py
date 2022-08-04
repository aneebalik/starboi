from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):

        if not email:
            raise ValueError('Email is mandatory.')
        
        if not username:
            raise ValueError('Username is required')
    

        user = self.model(
            email             =self.normalize_email(email),
            username          =username,
            first_name        =first_name,
            last_name         =last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email             =self.normalize_email(email),
            username          =username,
            first_name        =first_name,
            last_name         =last_name,
            password          =password
        )

        user.is_admin        =True
        user.is_active       =True
        user.is_staff        =True
        user.is_superadmin   =True
        user.save(using=self._db)
        return user


def get_profile_image_file(self, filename):
    return 'profile_image/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return "images/icons/favicon.png"




class Account(AbstractBaseUser):
    first_name          =models.CharField(max_length=50)
    last_name           =models.CharField(max_length=50)
    username            =models.CharField(max_length=50,unique=True)
    email               =models.EmailField(max_length=150,unique=True)
    phone_number        =models.CharField(max_length=60)
    profile_image		=models.ImageField(max_length=255, upload_to=get_profile_image_file, null=True, blank=True, default=get_default_profile_image)
    
    hide_email		    = models.BooleanField(default=True)
    date_joined         =models.DateTimeField(auto_now_add=True)
    last_login          =models.DateTimeField(auto_now_add=True)
    is_admin            =models.BooleanField(default=False)
    is_staff            =models.BooleanField(default=False)
    is_active           =models.BooleanField(default=False)
    is_superadmin       =models.BooleanField(default=False)

    
    USERNAME_FIELD      ='email'
    REQUIRED_FIELDS     =['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email and self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin    

    def has_module_perms(self, add_label):
        return True
    
    def get_profile_image_filename(self):
        return str(self.profile_picture)[str(self.profile_picture).index('profile_image/' + str(self.pk) + "/"):]
		

class UserProfile(models.Model):
    user           = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture= models.ImageField(blank=True, null=True, upload_to = 'userprofile')
    city           = models.CharField(blank=True, max_length=20)
    state          = models.CharField(blank=True, max_length=20)
    country        = models.CharField(blank=True,max_length=20)


    def __str__(self):
        return self.user.first_name

    def full_adress(self):
        return f'{self.address_line_1} {self.address_line_2}'