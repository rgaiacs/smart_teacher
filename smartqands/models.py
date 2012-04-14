from django.db import models

# Create your models here.
class SmartQAndS(models.Model):
    """
    It's used to generate the interact version.
    """
    arg = models.TextField('Arguments', blank=True)
    des = models.TextField('Description')
    question = models.TextField('Question')
    solution = models.TextField('Solution', blank=True)
    ref = models.TextField('Reference', blank=True)
    key = models.ManyToManyField('Keyword', blank=True, verbose_name='Keywords')

    def __unicode__(self):
        return u'%s' % (self.question)

class Keyword(models.Model):
    """
    Keywords for SmartQAndS.
    """
    key = models.CharField('Keyword', primary_key=True, max_length=100)
    up = models.ForeignKey('Keyword', verbose_name='More general keyword')

    def __unicode__(self):
        return u'%s' % (self.key)
