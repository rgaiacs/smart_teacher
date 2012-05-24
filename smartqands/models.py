from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SmartQAndS(models.Model):
    """
    It's used to generate the interact version.
    """
    description = models.CharField('Description', unique=True, max_length=255, help_text="")
    category = models.ManyToManyField('Category', blank=True, verbose_name='Category')
    keyword = models.ManyToManyField('Keyword', blank=True, verbose_name='Keywords')
    counter = models.IntegerField('Counter', help_text="")
    is_redirect = models.BooleanField('Is redirect', help_text="")
    lastest = models.ForeignKey('Revision', related_name='revision_lastest', blank=True, null=True, verbose_name='Category')

    def __unicode__(self):
        return u'{0}'.format(self.des)

class Revision(models.Model):
    script = models.OneToOneField('Script')
    smartqands = models.ForeignKey('SmartQAndS')
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

class Script(models.Model):
    # arg = models.TextField('Arguments', blank=True)
    # question = models.TextField('Question')
    # solution = models.TextField('Solution', blank=True)
    interact = models.TextField('Interact')

    def __unicode__(self):
        return u'{0}'.format(self.interact)

class Image(models.Model):
    pass

class Restrictions(models.Model):
    pass

class Category(models.Model):
    title = models.CharField('Category', primary_key=True, max_length=100)
    parent = models.ForeignKey('Category', verbose_name='More general category', null=True)

    def __unicode__(self):
        return u'%s' % (self.title)

class Keyword(models.Model):
    """
    Keywords for SmartQAndS.
    """
    title = models.CharField('Keyword', primary_key=True, max_length=100)

    def __unicode__(self):
        return u'%s' % (self.title)

class Comment(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    smartqands = models.ForeignKey('SmartQAndS')
    comment = models.TextField('Comment')
    pass

class LangLinks(models.Model):
    pass

class Redirect(models.Model):
    pass
