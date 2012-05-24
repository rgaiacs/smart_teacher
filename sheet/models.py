from django.db import models
from django.contrib.auth.models import User
from smartqands.models import SmartQAndS

# Create your models here.
class Sheet(models.Model):
    """
    It's used to keep track of related qands.
    """
    user = models.ManyToManyField(User)
    title = models.CharField('Title', unique=True, max_length=255, help_text="")
    description = models.TextField('Description', blank=True)
    is_public = models.BooleanField('Is public', help_text="")

    def __unicode__(self):
        return u'%s_%s' % (self.user, self.title)

class QAndS(models.Model):
    """
    It's used to generate the static version.
    """
    sheet = models.ForeignKey(Sheet)
    smartqands = models.ForeignKey(SmartQAndS)
    arg = models.TextField('Arguments', blank=True)
    question = models.TextField('Question')
    solution = models.TextField('Solution', blank=True)

    def __unicode__(self):
        return u'%s' % (self.question)
