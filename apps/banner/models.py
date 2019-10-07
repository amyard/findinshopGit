from django.db import models

class Banner(models.Model):
    """
    Full info about banner
    """
    user = models.ForeignKey('auth.User', related_name='banners')
    image = models.ImageField(upload_to='banners')
    active = models.BooleanField()
    count = models.IntegerField()
    redirect = models.URLField()
    date_add = models.DateTimeField(verbose_name=u'Date', auto_now_add=True)

    def __unicode__(self):
        return u'%s: %s' % (self.user, self.image)

    class Meta:
        unique_together = ('user', 'image')