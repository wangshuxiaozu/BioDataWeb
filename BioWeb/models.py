from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class User(models.Model):
	nid=models.AutoField(primary_key=True)
	name=models.CharField(max_length=20)
	passwd=models.CharField(max_length=50)
	school=models.CharField(max_length=20)
	shcoolID=models.IntegerField()
	emial=models.EmailField()
	phone=models.BigIntegerField()
	add_date = models.DateTimeField('保存日期',default = timezone.now)
	mod_date = models.DateTimeField('最后修改日期', auto_now=True)

	def __unicode__(self):
		return self.name
class Update_file(models.Model):
	nid=models.AutoField(primary_key=True)
	xid=models.IntegerField(default=0)
	userid=models.ForeignKey(User,on_delete=models.CASCADE)
	LOCUS=models.CharField(max_length=50,default="")
	DEFINITION=models.CharField(max_length=500,default="")
	CDS=models.CharField(max_length=100,default="")
	translation=models.TextField(default="")
	ORIGIN=models.TextField(default="")
	add_date = models.DateTimeField('保存日期',default = timezone.now)
	def __unicode__(self):
		return self.LOCUS
class Update_images(models.Model):
	nid=models.AutoField(primary_key=True)
	userid=models.ForeignKey(Update_file,on_delete=models.CASCADE)
	Aimg= models.CharField(max_length=50,default="")
	Timg= models.CharField(max_length=50,default="")
	Cimg= models.CharField(max_length=50,default="")
	Gimg= models.CharField(max_length=50,default="")
	def __unicode__(self):
		return self.userid
class Statist_img(models.Model):
	nid=models.AutoField(primary_key=True)
	userid=models.ForeignKey(Update_file,on_delete=models.CASCADE)
	tongji_img= models.CharField(max_length=50,default="")
	def __unicode__(self):
		return self.userid
class perp_img(models.Model):
	nid=models.AutoField(primary_key=True)
	userid=models.ForeignKey(Update_file,on_delete=models.CASCADE)
	pertine_img=models.CharField(max_length=50,default="")
	def __unicode__(self):
		return self.userid