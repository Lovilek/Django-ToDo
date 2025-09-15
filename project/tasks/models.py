
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Tag(models.Model):
    name=models.CharField(max_length=64,unique=True)
    slug=models.SlugField(max_length=64,unique=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name,allow_unicode=True)
        return super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        NEW='new','New'
        IN_PROGRESS='in_progress','In progress'
        DONE='done','Done'

    class Priority(models.IntegerChoices):
        LOW=1,'Low'
        NORMAL=2,'Normal'
        HIGH=3,'High'

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    title=models.CharField(max_length=120)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=Status,default=Status.NEW)
    priority=models.IntegerField(choices=Priority,default=Priority.NORMAL)
    due_date=models.DateField(null=True,blank=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    tags=models.ManyToManyField(Tag,blank=True,related_name='tasks')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def is_overdue(self) -> bool:
        return (
            self.status != self.Status.DONE
            and self.due_date is not None
            and timezone.localdate() > self.due_date
        )

    def days_left(self):
        if self.due_date is None:
            return None
        return (self.due_date - timezone.localdate()).days


    def short_text(self,limit: int = 80) -> str:
        text=(self.description or '').strip()
        return text if len(text)<=limit else text[:limit-1]+"..."

    def __str__(self):
        return self.title






