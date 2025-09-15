from django.contrib import admin
from .models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')
    prepopulated_fields = {'slug':('name',)}
    search_fields = ('name',)
    ordering = ('id','name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','status','priority','due_date','is_overdue','created_at')
    list_filter = ('status','priority','due_date','created_at','tags')
    search_fields = ('title','description','owner__username')
    autocomplete_fields = ('owner','tags')
    readonly_fields = ('created_at','updated_at','completed_at')
    ordering = ('id','-created_at')