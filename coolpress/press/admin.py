from django.contrib import admin
from press.models import Category, Post, CoolUser


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    last_display = ('label', 'view_post_link', 'slug')


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author__user__username']
    list_display = ['title', 'author']
    date_hierarchy = 'creation_date'

admin.site.register(Post, PostAdmin)


class CoolUserAdmin(admin.ModelAdmin):
    pass


admin.register(CoolUser, CoolUserAdmin)
