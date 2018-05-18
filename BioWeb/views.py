from django.shortcuts import render
from django.http import HttpResponse
from BioWeb.models import *
from BioWeb.forms import *
import time
import os
from BioDataWeb.settings import BASE_DIR
import matplotlib.pyplot as plt
import numpy as np
import random
# Create your views here.
aname=random.uniform(1,1000)
apath='static/image/'+str(aname)
destination=os.path.join(BASE_DIR,apath).replace('\\', '/')
users=User.objects.all();
UpFile=Update_file.objects.all();
context={
'number':[i for i in range(10)],
'users':users,
'UpFile':UpFile,
}
def index(request):
	if request.method=='POST':
		form=UserForm(request.POST,request.FILES)
		if form.is_valid():
			username=form.cleaned_data['name']
			userpasswd=form.cleaned_data['passwd']
			user=User.objects.filter(name=username,passwd=userpasswd)
			if user:
				return render(request,'html5/major.html',context)
			else:
				return render(request,'html5/index.html',context)
	else:
		return render(request,"html5/index.html",context);
def major(request):
	if request.method == 'POST':# 获取对象
		files = request.FILES.get('myfile')
		myData=[]
		for i in files:
			i=i.strip()
			i=str(i)
			myData.append(i)
		FileData=camulate(myData)
		userid=User.objects.filter(nid=1)
		xid=len(Update_file.objects.all())+1;
		Update_file.objects.create(xid=xid,userid=userid[0],LOCUS=FileData['LOCUS'],DEFINITION=FileData['DEFINITION'],CDS=FileData['CDS'],translation=FileData['translation'],ORIGIN=FileData['ORIGIN'])
		DNA=str(FileData['ORIGIN'])
		create_img(DNA)
		images=Update_images.objects.last()
		context['images']=images
		UpFile=Update_file.objects.all();
		context['UpFile']=UpFile
		valumn=tongji(DNA)
		tongji_data=Statist_img.objects.last()
		CdsSequence=get_cds(DNA,FileData['CDS'])
		per_tu(FileData['translation'])
		perp_data=perp_img.objects.last()
		context['DNA']=Str_traslate_list(DNA)
		context['LOCUS']=FileData['LOCUS']
		context['CDS']=FileData['CDS']
		context['translation']=Str_traslate_list(FileData['translation'])
		context['CdsSequence']=Str_traslate_list(CdsSequence)
		context['valumn']=valumn
		context['tongji_data']=tongji_data
		context['perp_data']=perp_data
		context['images']=images
		context['HaveData']="文件上传成功！"
	else:
		context['HaveData']='无文件'
	return render(request,"html5/major.html",context);

def user(request):
	return render(request,"html5/user.html",context);
def login(request):
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['name']
			userpasswd=form.cleaned_data['passwd']
			user=User.objects.filter(name=username,passwd=userpasswd)
			context["HaveData"]=""
			if user:
				return render(request,'html5/major.html',context)
			else:
				return render(request,'html5/index.html',context)




def find_locate(needDatad,FileData):
	m=""
	for i in FileData:
		if i.find(needDatad)!=-1:
			m=i
			break
	m=m.split('  ')
	out=[]
	for i in m:
		if i!='':
			out.append(i)
	return out[1]
def camulate(FileData):
	needData=["LOCUS","DEFINITION","CDS","translation","ORIGIN"]
	SQLData={}
	for i in range(3):
		SQLData[needData[i]]=find_locate(needData[i],FileData)
	m=""
	bol=0
	j=0
	for i in FileData:
		i.strip()
		if bol==1:
			m=m+i
			if i.find('"')!=-1:
				break
		else :
			if i.find(needData[3])!=-1:
				bol=1
				m=i
	out=m.split('"')
	SQLData[needData[3]]=out[1]
	SQLData[needData[3]]=SQLData[needData[3]].replace("'","")
	SQLData[needData[3]]=SQLData[needData[3]].replace("b","")
	m=""
	bol=0
	j=0
	for i in FileData:
		i.strip()
		if i.find('//')!=-1:
			break
		if bol==1:
			f=i.split()
			for k in f[1:]:
				m=m+k.upper() 
		else :
			if i.find(needData[4])!=-1:
				bol=1
	SQLData[needData[4]]=m.replace("'","")
	return SQLData





def G_number(Gene,How):
	y=[]
	window_length=100
	length=""
	total=25
	zone=100
	sale=0.25
	i=1
	for G in Gene:
		if i<=100:
			length=length+G
			if G==How:
				sale=sale+1/100
			else:
				sale=sale-1/400
		else:
			length=length[1:]+G
			total=length.count(How)
			sale=total/zone
		y.append(sale)
		i=i+1
	return y  
def create_img(Gene):  
	global apath    
	import os
	x1=[x for x in range(len(Gene))]
	always=[]
	for How in ['A','T','C','G']:
	    always.append(G_number(Gene,How))

	atcg=['A=black','T=blue','C=red','G=green']
	#Aimg
	k=plt.plot(x1,always[0],linewidth=1,color='k') 
	plt.xlim(0,len(Gene))
	plt.xlabel('Plot Number') 
	plt.ylabel('Important var') 
	plt.title('Interesting Graph\nCheck it out') 
	plt.legend(atcg[0:1],loc='upper center')
	plt.savefig(destination+"Aimg.png")
	#Timg
	plt.plot(x1,always[0],linewidth=1,color='k') 
	plt.plot(x1,always[1],linewidth=1,color='b')
	plt.xlim(0,len(Gene))
	plt.xlabel('Plot Number') 
	plt.ylabel('Important var') 
	plt.title('Interesting Graph\nCheck it out') 
	plt.legend(atcg[0:2],loc='upper center')
	plt.savefig(destination+"Timg.png")
	#Cimg
	plt.plot(x1,always[0],linewidth=1,color='k') 
	plt.plot(x1,always[1],linewidth=1,color='b')
	plt.plot(x1,always[2],linewidth=1,color='r')
	plt.xlim(0,len(Gene))
	plt.xlabel('Plot Number') 
	plt.ylabel('Important var') 
	plt.title('Interesting Graph\nCheck it out') 
	plt.legend(atcg[0:3],loc='upper center')
	plt.savefig(destination+"Cimg.png")
	#Gimg
	plt.plot(x1,always[0],linewidth=1,color='k') 
	plt.plot(x1,always[1],linewidth=1,color='b')
	plt.plot(x1,always[2],linewidth=1,color='r')
	plt.plot(x1,always[3],linewidth=0.5,color='g')
	plt.xlim(0,len(Gene))
	plt.xlabel('Plot Number') 
	plt.ylabel('Important var') 
	plt.title('Interesting Graph\nCheck it out') 
	plt.legend(atcg[0:4],loc='upper center')
	plt.savefig(destination+"Gimg.png")
	userid=Update_file.objects.last()
	apath="/"+apath
	Update_images.objects.create(userid=userid,Aimg=apath+"Aimg.png",Timg=apath+"Timg.png",Cimg=apath+"Cimg.png",Gimg=apath+"Gimg.png")



def tongji(dna):
	global apath
	import matplotlib.pyplot as plt
	import numpy as np
	from matplotlib import cm
	import random
	from matplotlib import cm
	key=['A','T','C','G','CG']
	value=[]
	for j in key:
		m=dna.count(j)
		value.append(m)
	obs=np.array(value)/len(dna)
	obs_exp=obs/0.25
	obs=obs.tolist()
	obs_exp=obs_exp.tolist()
	plt.figure()
	ax1=plt.subplot(111)
	label =key
	value=np.array(value)
	width=0.5
	x_bar=np.arange(5)
	color=[random.uniform(0,1) for _ in range(5)]
	color = cm.jet(np.array(color))
	rect=ax1.bar(key,value,width=width,color=color)
	for rec in rect:
		x=rec.get_x()
		height=rec.get_height()
		ax1.text(x+0.1,1.02*height,str(height))
	ax1.set_xticks(x_bar)
	ax1.set_ylabel("sales")
	ax1.set_title("The Sales in 2018")
	ax1.grid(True)
	ax1.set_ylim(0,max(value)+200)

	plt.savefig(destination+"tongji_img.png")
	userid=Update_file.objects.last()
	Statist_img.objects.create(userid=userid,tongji_img=apath+"tongji_img.png")
	valumn=[]
	for i in range(len(key)):
		valumn.append([key[i],obs[i],obs_exp[i]])
	return valumn


def get_cds(x,CDS):
	x=x.replace('\n','')
	x=x.replace(' ','')
	m=CDS[CDS.find('(')+1:CDS.find(')')]
	m=m.replace('..','-')
	allCDS=m.split(',')
	CDS=""
	for n in allCDS :
	    left_right=n.split('-')
	    a=int(left_right[0])-1
	    b=int(left_right[1])-1
	    type(a)
	    while a<=b:
	        CDS+=x[a]
	        a+=1
	return CDS


def Str_traslate_list(words):
	zimu=[]
	for i in words:
		zimu.append(i)
	return zimu


def per_tu(pretine):
	global apath
	from collections import Counter
	f=Counter(pretine)
	key=[]
	value=[]
	for i in f:
		key.append(i)
		value.append(f[i])
	import numpy as np    
	import matplotlib.mlab as mlab    
	import matplotlib.pyplot as plt    
	labels=key  
	X=value   
	fig = plt.figure()  
	plt.pie(X,labels=labels,autopct='%1.2f%%') 
	plt.title("exp chart")
	plt.savefig(destination+"pertine_img.png")
	userid=Update_file.objects.last()
	perp_img.objects.create(userid=userid,pertine_img=apath+"pertine_img.png")   
'''
def dddd_major(request):
	if request.method=='POST':
		obj=UpdateForm(request.FILES)
		if obj.is_valid():
			files=obj.cleaned_data['myfile']
			if files:
				aname=files.name
				myData=[]
				for i in files:
					myData.append(str(i))
				context['HaveData']="上传成功！"
				return render(request,"html5/major.html",context);
				aname=str(time.time())
				apath='static/file/'+aname
				destination=open(os.path.join(BASE_DIR,apath).replace('\\', '/'),'wb')
				count=Update_file.objects.create(name=aname,path=apath,userid_id=1)  
				if count:
					return render(request, 'html5/major.html', context);
				else:
					context['HaveData']='数据上传失败！'
					return render(request,"html5/major.html",context);
		else:
			context['HaveData']='无文件'
			return render(request,"html5/major.html",context);
	else:
		return HttpResponse("hello wrold!")
'''