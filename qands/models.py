from django.db import models
from sheet.models import Sheet
from smartqands.models import SmartQAndS

# Create your models here.
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
