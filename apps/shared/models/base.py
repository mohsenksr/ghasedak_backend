from django.db import models
from django.db.models import Manager


class BaseModelManager(Manager):
    def all(self):
        return self.filter(archived=False)


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey(to='account.User', on_delete=models.SET_NULL, null=True, blank=True)
    archived = models.BooleanField(default=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True
        ordering = ["-modified_date"]

    def generate(self, **kwargs):
        return


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
