from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from recipeShareApp.models import *
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
import json
import base64
import string
import logging
import pickle

from django.http import HttpResponseRedirect
from .forms import MessageForm
from django.core import serializers
from django.forms.models import model_to_dict

from .serializers import MessageSerializer
from rest_framework import viewsets

from django.template import RequestContext

# Create your views here.
def need_auth(functor):
    def try_auth(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            basicauth = request.META['HTTP_AUTHORIZATION']
            user = None
            try:
                b64key = basicauth.split(' ')[1]
                #key = base64.decodestring(b64key)
                key = base64ToString(b64key)
                (username,pw) = key.split(':')
                user = authenticate(username=username,password=pw)
            except:
                pass
 
            if user is not None:
                login(request, user)
                request.META['user'] = user
                return functor(request, *args, **kwargs)
 
        logout(request)
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="recipeShareApp Service"'
        return response
    return try_auth


 
def serve_html(reqeust, page):
    #return render_to_response(page+'.html')
    return render(reqeust, page+'.html')


@need_auth
def login_view(request):
    return toJSON({'status': 'OK', 'user':request.user.userprofile.serialize()})
 

@need_auth
def profile_view(request, username=None):
    if username == None:
        username = request.user
    
    if request.method == 'GET':
        try:
            userprofile = User.objects.get(username=username).userprofile
            return toJSON(userprofile.serialize())
            
        except:
            return toJSON({'status': 'not found'}, 400)
        
    elif request.method == 'POST':
        profile = request.user.userprofile
        profile.nickname = request.POST.get('nickname', profile.nickname)
        profile.comment = request.POST.get('comment', profile.comment)
        profile.country = request.POST.get('country', profile.country)
        profile.url = request.POST.get('url', profile.url)
        ignores = request.POST.get('ignore', None)
        if ignores:
            ignores = json.loads(ignores)
            profile.set_ignorelist(ignores)
        
        profile.save()
        
        return toJSON({'status': 'updated'})

'''
@need_auth
def profile_view(request, username):
    if request.method == 'GET':
        try:
            userprofile = User.objects.get(username=username).userprofile
            return toJSON(userprofile.serialize())
            
        except:
            return toJSON({'status': 'not found'}, 400)
'''

@need_auth
def checkpassword_view(request):
    try:
        password = request.POST.get('password')
        if request.user.check_password(password):
            return toJSON({'status': 'OK'})
        
    except:
        pass
    return toJSON({'status': 'no'})
 
@need_auth
def setpassword_view(request):
    try:
        password = request.POST.get('password')
        if password:
            request.user.set_password(password)
            request.user.save()
            return toJSON({'status': 'OK'})
        
    except:
        pass
    
    return toJSON({'status': 'no'})

@need_auth
def name_view(request):
    if request.method == 'GET':
        data = {
            'name': request.user.first_name,
        }
        
        return toJSON(data)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            request.user.first_name = name
            request.user.save()
            
            return toJSON({'status': 'updated'})
            
        except:
            return toJSON({'status': 'bad request'}, 400)


@need_auth
def find_view(request):
    query = request.GET.get('query', '')
    
    #result = Message.objects.filter(Q(message__contains=query)|Q(user__userprofile__nickname__contains=query))
    result = Message.objects.filter(message__contains=query)
 
    return toJSON(serialize(result))


@need_auth
def like_view(request, num):
    try:
        message = Message.objects.get(id=num)
        like = Like()
        like.user = request.user
        like.message = message
        like.save()
        
    except:
        return toJSON({'status': 'bad request'}, 400)
    
    return toJSON({'status': 'created'})



@need_auth
def message_delete_view(request, num):
    try:
        message = Message.objects.get(id = num)
        if message.user == request.user:
            message.delete()
            return toJSON({'status': 'deleted'})
        else:
            return toJSON({'status': 'forbidden'}, 401)
        
    except:
        return toJSON({'status': 'not found'}, 400)


@need_auth
def message_view(request, num):
    try:
        message = Message.objects.get(id = num)
        
        return toJSON(message.serialize())
        
    except:
        return toJSON({'status': 'not found'}, 400)
    
    return HttpResponse(None)

@need_auth
def message_create_view(request):
    if request.method != 'POST':
        return toJSON({'status': 'bad request'}, 400)
    
    message = Message()
    
    #message = MessageForm(request.POST, request.FILES)
    
    #form =  UploadFileForm(request.POST, request.FILES)
    
    #print "photo",  request.FILES["image"]
    
    
    try:

        message.user = request.user
        message.message = request.POST.get('message', '')
        #message.message = request.FILES.getlist('photo')
        #message.photo = request.FILES['files_send']
        #message.photo = request.FILES['photo']
        #print "message.photo",  request.FILES["image"]
        #message.photo = request.FILES.getlist('photo')
        #message.photo = request.FILES.get('photo')
        #message.photo = request.FILES('photo')
        #message.photo = request.POST.get('blah', '')
        #message.photo = request.FILES.get('photo','')
        #message.photo = request.FILES["photo"]
        #message.photo = request.FILES["image"] #this
        #message.photo = request.FILES['image']
        if 'image' in request.FILES: 
            message.photo = request.FILES['image'] #print "exist"
        #else :
        #    print "none"
        
        #print "message.photo",  message.photo
        #message.photo = request.FILES["image"]["name"]
        #message.photo = UploadFileForm(request.POST, request.FILES)
        #message.photo = form
        
        message.masterTitle = request.POST.get('masterTitle', '')
        message.memeo = request.POST.get('memeo', '')
        message.bean = request.POST.get('bean', '')
        message.temperature = request.POST.get('temperature', '')
        message.address = request.POST.get('address', '')
        message.amt00 = request.POST.get('amt00', '')
        message.amt01 = request.POST.get('amt01', '')
        message.amt02 = request.POST.get('amt02', '')
        message.amt03 = request.POST.get('amt03', '')
        message.amt04 = request.POST.get('amt04', '')
        message.amt05 = request.POST.get('amt05', '')
        message.amt06 = request.POST.get('amt06', '')
        message.amt07 = request.POST.get('amt06', '')
        message.amt08 = request.POST.get('amt07', '')
        message.amt09 = request.POST.get('amt08', '')
        message.amt10 = request.POST.get('amt10', '')
        message.btime00 = request.POST.get('btime00', '')
        message.btime01 = request.POST.get('btime01', '')
        message.btime02 = request.POST.get('btime02', '')
        message.btime03 = request.POST.get('btime03', '')
        message.btime04 = request.POST.get('btime04', '')
        message.btime05 = request.POST.get('btime05', '')
        message.btime06 = request.POST.get('btime06', '')
        message.btime07 = request.POST.get('btime07', '')
        message.btime08 = request.POST.get('btime08', '')
        message.btime09 = request.POST.get('btime09', '')
        message.btime10 = request.POST.get('btime10', '')
        message.itime00 = request.POST.get('itime00', '')
        message.itime01 = request.POST.get('itime01', '')
        message.itime02 = request.POST.get('itime02', '')
        message.itime03 = request.POST.get('itime03', '')
        message.itime04 = request.POST.get('itime04', '')
        message.itime05 = request.POST.get('itime05', '')
        message.itime06 = request.POST.get('itime06', '')
        message.itime07 = request.POST.get('itime07', '')
        message.itime08 = request.POST.get('itime08', '')
        message.itime09 = request.POST.get('itime09', '')
        message.itime10 = request.POST.get('itime10', '')
        message.totAmt = request.POST.get('totAmt', '')
        message.totMin = request.POST.get('totMin', '')
        message.totSec = request.POST.get('totSec', '')     
        
        message.save()
        
        
        return toJSON({'status': 'create success'})
        
    except:
        return toJSON({'status': 'bad request'}, 400)
    

    
def upload_file(request):
    print "upload start", form
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        print "form", form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = MessageForm()
    #return render(request, 'upload.html', {'form': form})
    return render(request, 'timeline.html', {'form': form})

    
'''
@need_auth
def recipeShareApp_view(request):
    messages = Message.objects.order_by('-created').all()
    #messages = Message.objects.all()
    ignore = request.user.userprofile.get_ignorelist()
    messages = messages.exclude(user__id__in = ignore)
    
    try:
        tweet_per_page = int(request.GET.get('per_page', 10))
        page_num = int(request.GET.get('page', 1))
        
        pages = Paginator(messages, tweet_per_page)
        
        resp = {
            'total_page': pages.num_pages,
            'total_count': pages.count,
            'messages': serialize(pages.page(page_num).object_list)
            #'messages': serialize()
        }
        
        return toJSON(resp)
    
    except:
        resp = {
            'status': 'pagination error'
        }
        return toJSON(resp, 400)
'''

def list_class_properties(cls):
    return [k for k,v in cls.__dict__.iteritems() if type(v) is property]

class recipeShareApp_view_Set(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    #print "queryset: ",  queryset
    #print "serializer_class: ",  serializer_class
    #print "serializer_class_data: ",  serializer_class.data
    
@need_auth
def recipeShareApp_view(request):
    #queryset = Message.objects.all()
    #messages = Message.objects.order_by('-created').all()
    #queryset = Message.objects.order_by('-created').all()#Message(data=request.DATA, files=request.FILES)
    #serializer_class = MessageSerializer   
    
    #serializer = Message(data=request.DATA, files=request.FILES)
    
    #messages = serializer
    messages = Message.objects.order_by('-created').all()

    #print "messages1: ",  messages
    #messages = Message.objects.all()
    ignore = request.user.userprofile.get_ignorelist()
    messages = messages.exclude(user__id__in = ignore)
    #messages1 = serializers.serialize("json", messages)
    

    #dat = serializers.serialize("json", messages)
    


    try:
        tweet_per_page = int(request.GET.get('per_page', 3))
        page_num = int(request.GET.get('page', 1))
        
        pages = Paginator(messages, tweet_per_page)
        

        #dat = serializers.serialize('json',pages.page(page_num).object_list)
        #dat = serializers.serialize('json',pages.page(page_num).object_list, fields=['photo'])
        #dat = serializers.serialize('json',pages.page(page_num).object_list)
        #dat = serializers.serialize('json',pages.page(page_num).object_list)
        
        #print "messages", pages.page(page_num).object_list
        
        #print "message : ", serialize(pages.page(page_num).object_list)
        #pickledump = list_class_properties(messages)
        #print "pickledump : ", pickledump
        #print "dat : ", dat

        #print "obj list : ", pages.page(page_num).object_list
        resp = {
            'total_page': pages.num_pages,
            'total_count': pages.count,
            'messages': serialize(pages.page(page_num).object_list),
            #'photo': dat
            #'messages': serialize()
            #'messages': dat
        }
        
        #dat = serializers.serialize("json", pages.page(page_num).object_list)

        #resp = serialize(pages.page(page_num).object_list)
        #print "messages: ",  messages
        #print "resp: ",  resp
        #data = serializers.serialize("json", tasks)
        #return HttpResponse(data, content_type='application/json')
        #return toJSONOBJ(resp)
        #return toJSONOBJ(resp)    
        #return toJSON(resp)
        return toJSONOBJ(resp)
        #return render_to_response(resp)
        #return render_to_response('timeline.html', {'messages': messages}, context_instance=RequestContext(request))
        #return render_to_response("timeline.html", {"messages": messages})
    
    except:
        resp = {
            'status': 'pagination error'
        }

        return toJSON(resp, 400)

@need_auth
def recipeShareApp_view_page(request, num):

    messages = Message.objects.order_by('-created').all()

    ignore = request.user.userprofile.get_ignorelist()
    messages = messages.exclude(user__id__in = ignore)


    try:
        tweet_per_page = int(request.GET.get('per_page', 1))
        page_num = int(request.GET.get('page', num))
        
        pages = Paginator(messages, tweet_per_page)

        resp = {
            'total_page': pages.num_pages,
            'total_count': pages.count,
            'messages': serialize(pages.page(page_num).object_list),

        }

        return toJSONOBJ(resp)
    
    except:
        resp = {
            'status': 'pagination error'
        }

        return toJSON(resp, 400)
    
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
'''
def recipeShareApp_view(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        
        auth = request.META['HTTP_AUTHORIZATION']
        print ( 'auth : ', auth )
        #key = base64.decodestring(auth.split(' ')[1])
        key = base64ToString(auth.split(' ')[1])
        print ( 'key : ', key )
        id, pw = key.split(':')
        print ( 'id : ', id )
        print ( 'pw : ', pw )
        if id == 'ChoiInseon' and pw == 'qwer':
            return HttpResponse('Hello id: %s, pwd: %s' %(id, pw))
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="recipeShareApp Service"'
    return response
'''
#@need_auth
def user_view(request, method):
    if method == 'create' and request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if User.objects.filter(username__exact=username).count():
                return HttpResponse('duplicate id', 400)
            user = User.objects.create_user(username, password=password)
            user.first_name = request.POST.get('name', '')
            user.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
            return toJSON({'status':'create Success'})
        except:
            return toJSON({'status':'create failed'}, 400)
    elif method == 'update' and request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            newpassword = request.POST.get('newpassword')
            user = User.objects.get(username__exact = username)
            if user.check_password(password) is False:
                return toJSON({'status':'wrong password'}, 400)
            else:
                user.set_password(newpassword)
                user.first_name = request.POST.get('name', user.first_name)
                user.save()
        except:
            return toJSON({'status':'bad request'}, 400)
        return toJSON({'status':'updated'})
    
    elif method == 'list':
        users = UserProfile.objects.all()
        return toJSON(serialize(users))
        
    else:
        return toJSON({'status':'bad request'}, 400)



def serialize(objs):
    #print "serialize objs", objs
    #return map(lambda x:x.serialize(), objs)
    return map(lambda x:x.serialize(), objs)
    #objs = serializers.serialize('json', self.get_queryset())
    #return map(lambda x:x.serialize(), objs)

 
def toJSON(objs, status=200):
    j = json.dumps(objs, encoding="utf-8", ensure_ascii=False)
    #j = json.dumps(objs)
    #j = serializers.serialize('json', self.get_queryset())
    return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')
    #return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')
    #return HttpResponse(json.simplejson.dumps(list(self.get_queryset())),
    #                    mimetype="application/json")
    #data = serializers.serialize('json', self.get_queryset())
    #return HttpResponse(data, content_type="application/json")
    
def toJSONOBJ(objs, status=200):
    #data = model_to_dict(objs)
    #print "data1", data
    #data['photo'] = data['photo'].url
    #print "data2", data


    j = json.dumps(objs, encoding="utf-8", ensure_ascii=False)
    #j = json.dumps( {'photo' : objs.encode('base64')}, encoding="utf-8", ensure_ascii=False)
    #j = json.dumps(objs, encoding="utf-8", ensure_ascii=False)
    #json.dumps({'picture' : data.encode('base64')})
    #print "dump file: " , objs
    
    return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')

    #return HttpResponse(json.dumps(data), content_type='application/json')
    #model = get_object_or_404(Message, id=id, user=1)
    #print "model", model
    #data = model_to_dict(model)
    #data = model_to_dict(objs)
    #print "data1", data
    #data['photo'] = data['photo'].url
    #print "data2", data
    #return HttpResponse(json.dumps(data), content_type='application/json')

'''    
    j = json.dumps(str(objs), encoding="utf-8", ensure_ascii=False)
    #j = json.dumps(objs, encoding="utf-8", ensure_ascii=False)
    #j = json.dumps(objs)
    #j = serializers.serialize('json', self.get_queryset())
    print "objs unicode---------", j

    #print "queryset-----------", self.get_queryset()
    
    print "return!!!!!!!!!!!!!!"
    
    return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')
'''



    #return HttpResponse(j, status=status, content_type='application/json; charset=utf-8')
    #return HttpResponse(json.simplejson.dumps(list(self.get_queryset())),
    #                    mimetype="application/json")
    #data = serializers.serialize('json', self.get_queryset())
    #return HttpResponse(data, content_type="application/json")

