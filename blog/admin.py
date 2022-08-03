from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug' : ('title',)}
    list_display        =('title','slug','body',)

admin.site.register(Post,PostAdmin)
