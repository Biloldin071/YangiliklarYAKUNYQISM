from django.contrib import admin
from .models import News, Category, Contact, Comment


# admin.site.register(News)
# admin.site.register(Category)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'status', 'publish_time']
    list_filter = ['status', 'created_time', 'publish_time', 'category']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'body']
    date_hierarchy = 'created_time'

@admin.register(Category)
class NewsCategory(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Contact)
class Category(admin.ModelAdmin):
    list_display = ['name','email','message']
    list_filter = ['name','email']





# admin.site.register(Contact)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['body', 'user']
    actions = ['disable_comment', 'enable_comment']

    def disable_comment(self, request, queryset):
        queryset.update(active = False)


    def enable_comment(self, request, queryset):
        queryset.update(active = True)