from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your models here.
 

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=128)
    comment = models.TextField()
    country = models.CharField(max_length=128, blank=True)
    url = models.CharField(max_length=128, blank=True)
    ignores = models.ManyToManyField(User, related_name='ignore_set', blank=True, null=True)
    
    def __unicode__(self):
        return "%s" % (self.user,)
    
   
    def get_ignorelist(self):
        ignores = []
        for k in self.ignores.all():
            ignores.append(k.id)
        return ignores
    
    def set_ignorelist(self, ignores):
        self.ignores = []
        for k in ignores:
            try:
                ignore = User.objects.get(id = k)
                self.ignores.add(ignore)
                self.save()
                
            except:
                pass
    def serialize(self):
        data = {
            'user': self.user_id,
            'username': self.user.username,
            'nickname': self.nickname,
            'comment': self.comment,
            'country': self.country,
            'url': self.url,
            'ignores': self.get_ignorelist(),
        }
        return data


class Message(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(null=True, blank=True, max_length=128)
    #photo = models.ImageField(null=True, blank=True, upload_to="photo/%Y/%m/%d")
    #photo = models.ImageField(storage=FileSystemStorage(location=settings.MEDIA_ROOT), upload_to="photo/%Y/%m/%d", default="settings.MEDIA_ROOT/Chrysanthemum.jpg")
    photo = models.ImageField(null=True, blank=True, upload_to="photo/%Y/%m/%d", default="brewvieDefault.jpg")
    created = models.DateTimeField(auto_now_add=True)   
    
    masterTitle = models.CharField(null=True, blank=True, max_length=8)
    memeo = models.TextField(null=True, blank=True)
    bean = models.CharField(null=True, blank=True, max_length=2) 
    temperature = models.CharField(null=True, blank=True, max_length=2)
    address = models.CharField(null=True, blank=True, max_length=3)
    amt00 = models.CharField(null=True, blank=True, max_length=3)
    amt01 = models.CharField(null=True, blank=True, max_length=3)
    amt02 = models.CharField(null=True, blank=True, max_length=3)
    amt03 = models.CharField(null=True, blank=True, max_length=3)
    amt04 = models.CharField(null=True, blank=True, max_length=3)
    amt05 = models.CharField(null=True, blank=True, max_length=3)
    amt06 = models.CharField(null=True, blank=True, max_length=3)
    amt07 = models.CharField(null=True, blank=True, max_length=3)
    amt08 = models.CharField(null=True, blank=True, max_length=3)
    amt09 = models.CharField(null=True, blank=True, max_length=3)
    amt10 = models.CharField(null=True, blank=True, max_length=3)
    btime00 = models.CharField(null=True, blank=True, max_length=2)
    btime01 = models.CharField(null=True, blank=True, max_length=2)
    btime02 = models.CharField(null=True, blank=True, max_length=2)
    btime03 = models.CharField(null=True, blank=True, max_length=2)
    btime04 = models.CharField(null=True, blank=True, max_length=2)
    btime05 = models.CharField(null=True, blank=True, max_length=2)
    btime06 = models.CharField(null=True, blank=True, max_length=2)
    btime07 = models.CharField(null=True, blank=True, max_length=2)
    btime08 = models.CharField(null=True, blank=True, max_length=2)
    btime09 = models.CharField(null=True, blank=True, max_length=2)
    btime10 = models.CharField(null=True, blank=True, max_length=2)
    itime00 = models.CharField(null=True, blank=True, max_length=2)
    itime01 = models.CharField(null=True, blank=True, max_length=2)
    itime02 = models.CharField(null=True, blank=True, max_length=2)
    itime03 = models.CharField(null=True, blank=True, max_length=2)
    itime04 = models.CharField(null=True, blank=True, max_length=2)
    itime05 = models.CharField(null=True, blank=True, max_length=2)
    itime06 = models.CharField(null=True, blank=True, max_length=2)
    itime07 = models.CharField(null=True, blank=True, max_length=2)
    itime08 = models.CharField(null=True, blank=True, max_length=2)
    itime09 = models.CharField(null=True, blank=True, max_length=2)
    itime10 = models.CharField(null=True, blank=True, max_length=2)
    totAmt = models.CharField(null=True, blank=True, max_length=3)
    totMin = models.CharField(null=True, blank=True, max_length=2)
    totSec = models.CharField(null=True, blank=True, max_length=2)

    def serialize(self):
        data = {
            'id': self.id,
            'user': self.user_id,
            'username': self.user.username,
            'liked': self.like_set.count(),
            'message': self.message,
            'photo': self.photo.url,
            'created': self.created.ctime(),
            'masterTitle': self.masterTitle,
            'memeo': self.memeo,
            'bean': self.bean,
            'temperature': self.temperature,
            'address': self.address,
            'amt00': self.amt00,
            'amt01': self.amt01,
            'amt02': self.amt02,
            'amt03': self.amt03,
            'amt04': self.amt04,
            'amt05': self.amt05,
            'amt06': self.amt06,
            'amt07': self.amt07,
            'amt08': self.amt08,
            'amt09': self.amt09,
            'amt10': self.amt10,
            'btime00': self.btime00,
            'btime01': self.btime01,
            'btime02': self.btime02,
            'btime03': self.btime03,
            'btime04': self.btime04,
            'btime05': self.btime05,
            'btime06': self.btime06,
            'btime07': self.btime07,
            'btime08': self.btime08,
            'btime09': self.btime09,
            'btime10': self.btime10,
            'itime00': self.itime00,
            'itime01': self.itime01,
            'itime02': self.itime02,
            'itime03': self.itime03,
            'itime04': self.itime04,
            'itime05': self.itime05,
            'itime06': self.itime06,
            'itime07': self.itime07,
            'itime08': self.itime08,
            'itime09': self.itime09,
            'itime10': self.itime10,
            'totAmt': self.totAmt,
            'totMin': self.totMin,
            'totSec': self.totSec,        
        }
    
        return data

class Like(models.Model):
    user = models.ForeignKey(User)
    message = models.ForeignKey('Message')


# Create your models here.
