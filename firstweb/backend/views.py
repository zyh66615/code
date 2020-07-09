from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from django.middleware.csrf import get_token
from .models import Book, User, Pic, Post, Comment
from django.core.cache import cache
import os
from backend.tasks import crawl
import time

MEDIA_DIR = 'http://106.12.94.60:8000/media/'
BOOK_DIR = 'http://106.12.94.60:8000/media/books/'


def format_time(t):
    t = str(t)[:19]
    t = t.replace(' ', '-')
    t = t.replace(':', '-')
    T = t.split('-')
    s1 = T[0] + '年' + T[1] + '月' + T[2] + '日'
    s2 = T[3] + '时' + T[4] + '分' + T[5] + '秒'
    t = s1 + ' ' + s2
    return t


def check(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        response = {}
        request = args[0]
        get_token(request)
        data = json.loads(request.body)
        if cache.get(data.get('name')) != 1:
            response["msg"] = '登录超时，请重新登录!'
            response["error_num"] = -2
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
            return JsonResponse(response)
        cache.set(data.get('name'), 1, 60 * 5)
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            response["msg"] = str(e)
            response["error_num"] = -1
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
        return JsonResponse(response)

    return wrapper


@require_http_methods(["GET", "POST"])
@check
def download(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    user = User.objects.get(name=data.get('name'))
    flag = Book.objects.filter(book_name=data.get('book_name'), user_name=user).values('download')[0]['download']
    if flag == 1:
        upload = Book.objects.filter(book_name=data.get('book_name'), user_name=user).values('is_upload')[0][
            'is_upload']
        if upload == 1:
            name = Book.objects.filter(book_name=data.get('book_name'), user_name=user).values('title')[0]['title']
            response["url"] = BOOK_DIR + '上传/' + data.get('name') + '/' + name + '.txt'
            response["error_num"] = 1
        else:
            book_state = \
                Book.objects.filter(book_name=data.get('book_name'), user_name=user).values('book_state')[0][
                    'book_state']
            name = Book.objects.filter(book_name=data.get('book_name'), user_name=user).values('title')[0]['title']
            if book_state == 1:
                response["url"] = BOOK_DIR + '完整/' + data.get('book_name') + '/' + name + '.txt'
                response["error_num"] = 1
            else:
                response["url"] = BOOK_DIR + '不完整/' + data.get('book_name') + '/' + name + '.txt'
                response["error_num"] = 1
    else:
        response["msg"] = '未能爬取该书'
        response["error_num"] = -1
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def add_book(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    book = Book.objects.filter(book_name=data.get('book_name'), user_name=data.get('name'))
    if book.exists():
        response["msg"] = '已存在该书'
        response["error_num"] = 1
    else:
        user = User.objects.get(name=data.get('name'))
        response["msg"] = 'success'
        response["error_num"] = 0
        # thread = Thread(target=craw)
        # thread.start()
        print(1)
        crawl.delay(data.get('book_name'))
        print(2)
        book = Book(book_name=data.get('book_name'), user_name=user)
        book.save()
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def reply(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    p = Post(id=data.get('id'))
    comment = Comment(name=data.get('name'), answer_post=p, content=data.get('content'))
    comment.save()
    c = Comment.objects.all()
    post = Post.objects.all()
    j = json.loads(serializers.serialize("json", post))
    if c.exists():
        for i in j:
            k = Comment.objects.filter(answer_post=i['pk'])
            reply = []
            if k.exists():
                for K in k:
                    reply.append({'name': K.name, 'content': K.content, 'time': format_time(K.add_time), 'id': K.id})
                i['fields']['Reply'] = reply
            else:
                i['fields']['Reply'] = reply
    else:
        for i in j:
            reply = []
            i['fields']['Reply'] = reply
    response['list'] = j
    response["msg"] = 'success'
    response["error_num"] = 0
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def post(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    p = Post(user_name=data.get('name'), title=data.get('title'), content=data.get('input'))
    p.save()
    response["msg"] = 'success'
    response["error_num"] = 0
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def show_post(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    post = Post.objects.all()
    c = Comment.objects.all()
    j = json.loads(serializers.serialize("json", post))
    if c.exists():
        for i in j:
            k = Comment.objects.filter(answer_post=i['pk'])
            reply = []
            if k.exists():
                for K in k:
                    reply.append({'name': K.name, 'content': K.content, 'time': format_time(K.add_time), 'id': K.id})
                i['fields']['Reply'] = reply
            else:
                i['fields']['Reply'] = reply
    else:
        for i in j:
            reply = []
            i['fields']['Reply'] = reply
    response['list'] = j
    response["msg"] = 'success'
    response["error_num"] = 0
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'

    return response


@require_http_methods(["GET", "POST"])
@check
def show_book(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    books = Book.objects.filter(user_name=data.get('name'))
    i = 1
    for b in books:
        if os.path.exists('./media/books/完整/' + b.book_name):
            t = os.listdir('./media/books/完整/' + b.book_name)
            brief = ''
            if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
            b.download = 1
            b.book_state = 1
            b.title = t[0][:-4]
            b.intro = brief
            Book.objects.filter(id=b.id).update(download=1, book_state=1, title=t[0][:-4], intro=brief)
        elif os.path.exists('./media/books/不完整/' + b.book_name):
            t = os.listdir('./media/books/不完整/' + b.book_name)
            brief = ''
            if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
            b.download = 1
            b.book_state = 0
            b.title = t[0][:-4]
            b.intro = brief
            Book.objects.filter(id=b.id).update(download=1, book_state=-1, title=t[0][:-4], intro=brief)
        b.id = i
        i += 1
    response["list"] = json.loads(serializers.serialize("json", books))
    response["msg"] = 'success'
    response["error_num"] = 0
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def show_books(request):
    start = time.time()
    response = {}
    books = Book.objects.filter()
    i = 1
    for b in books:
        if os.path.exists('./media/books/完整/' + b.book_name):
            t = os.listdir('./media/books/完整/' + b.book_name)
            brief = ''
            if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
            b.download = 1
            b.book_state = 1
            b.title = t[0][:-4]
            b.intro = brief
            Book.objects.filter(id=b.id).update(download=1, book_state=1, title=t[0][:-4], intro=brief)
        elif os.path.exists('./media/books/不完整/' + b.book_name):
            t = os.listdir('./media/books/不完整/' + b.book_name)
            brief = ''
            if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
            b.download = 1
            b.book_state = 0
            b.title = t[0][:-4]
            b.intro = brief
            Book.objects.filter(id=b.id).update(download=1, book_state=-1, title=t[0][:-4], intro=brief)
        b.id = i
        i += 1
    response["list"] = json.loads(serializers.serialize("json", books))
    response["msg"] = 'success'
    response["error_num"] = 0
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def show_pic(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    pic = Pic.objects.filter(pic_name=data.get('name'))
    if pic.exists():
        response["img"] = MEDIA_DIR + 'images/' + data.get('name') + '.jpg'
    else:
        response["img"] = ''
    response["msg"] = 'success'
    response["error_num"] = 0
    response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def del_post(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    p = Post.objects.filter(id=data.get('id'))
    if p.exists():
        p.delete()
        post = Post.objects.all()
        c = Comment.objects.all()
        j = json.loads(serializers.serialize("json", post))
        if c.exists():
            for i in j:
                k = Comment.objects.filter(answer_post=i['pk'])
                reply = []
                if k.exists():
                    for K in k:
                        reply.append({'name': K.name, 'content': K.content, 'time': format_time(K.add_time), 'id': K.id})
                    i['fields']['Reply'] = reply
                else:
                    i['fields']['Reply'] = reply
        else:
            for i in j:
                reply = []
                i['fields']['Reply'] = reply
        response['list'] = j
        response["msg"] = 'success'
        response["error_num"] = 0
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    else:
        response["msg"] = '无此post'
        response["error_num"] = 2
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'

    return response


@require_http_methods(["GET", "POST"])
@check
def del_reply(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    c = Comment.objects.filter(id=data.get('id'))
    if c.exists():
        c.delete()
        post = Post.objects.all()
        c = Comment.objects.all()
        j = json.loads(serializers.serialize("json", post))
        if c.exists():
            for i in j:
                k = Comment.objects.filter(answer_post=i['pk'])
                reply = []
                if k.exists():
                    for K in k:
                        reply.append({'name': K.name, 'content': K.content, 'time': format_time(K.add_time), 'id': K.id})
                    i['fields']['Reply'] = reply
                else:
                    i['fields']['Reply'] = reply
        else:
            for i in j:
                reply = []
                i['fields']['Reply'] = reply
        response['list'] = j
        response["msg"] = 'success'
        response["error_num"] = 0
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    else:
        response["msg"] = '无此comment'
        response["error_num"] = 2
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return response


@require_http_methods(["GET", "POST"])
@check
def del_book(request):
    start = time.time()
    response = {}
    data = json.loads(request.body)
    if isinstance(data.get('book_name'), str):
        book_name = data.get('book_name')
        user_name = data.get('name')
        book = Book.objects.filter(book_name=book_name, user_name=user_name)
        if book.exists():
            if book.values('is_upload')[0]['is_upload'] == 1:
                print(book_name)
                p = './media/books/上传/' + user_name + '/' + book_name + '.txt'
                if os.path.exists(p):
                    os.remove(p)
            else:
                if book.values('download')[0]['download'] == 1:
                    if book.values('book_state')[0]['book_state'] == 1:
                        path = './media/books/完整/' + book_name + '/'
                        for p in os.listdir(path):
                            os.remove(path + p)
                        os.rmdir(path)
                    elif book.values('book_state')[0]['book_state'] == -1:
                        path = './media/books/不完整/' + book_name + '/'
                        for p in os.listdir(path):
                            os.remove(path + p)
                        os.rmdir(path)
                if os.path.exists('./media/books/简介/' + book_name + '.txt'):
                    os.remove('./media/books/简介/' + book_name + '.txt')
            book.delete()
            books = Book.objects.filter(user_name=user_name)
            i = 1
            for b in books:
                if os.path.exists('./media/books/完整/' + b.book_name):
                    t = os.listdir('./media/books/完整/' + b.book_name)
                    brief = ''
                    if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                        brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
                    b.download = 1
                    b.book_state = 1
                    b.title = t[0][:-4]
                    b.intro = brief
                    Book.objects.filter(id=b.id).update(download=1, book_state=1, title=t[0][:-4], intro=brief)
                elif os.path.exists('./media/books/不完整/' + b.book_name):
                    t = os.listdir('./media/books/不完整/' + b.book_name)
                    brief = ''
                    if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                        brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
                    b.download = 1
                    b.book_state = 0
                    b.title = t[0][:-4]
                    b.intro = brief
                    Book.objects.filter(id=b.id).update(download=1, book_state=-1, title=t[0][:-4], intro=brief)
                else:
                    b.book_state = -1
                    Book.objects.filter(id=b.id).update(download=0, book_state=-1)
                b.id = i
                i += 1
            response["list"] = json.loads(serializers.serialize("json", books))
            response["msg"] = 'success'
            response["error_num"] = 0
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
        else:
            response["msg"] = '无此书'
            response["error_num"] = 2
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    else:
        user_name = data.get('name')
        Books = data.get('book_name')
        for book_name in Books:
            book = Book.objects.filter(book_name=book_name, user_name=user_name, is_upload=Books[book_name])
            if book.exists():
                if book.values('is_upload')[0]['is_upload'] == 1:
                    p = './media/books/上传/' + user_name + '/' + book_name + '.txt'
                    if os.path.exists(p):
                        os.remove(p)
                else:
                    if book.values('download')[0]['download'] == 1:
                        if book.values('book_state')[0]['book_state'] == 1:
                            path = './media/books/完整/' + book_name + '/'
                            for p in os.listdir(path):
                                os.remove(path + p)
                            os.rmdir(path)
                        elif book.values('book_state')[0]['book_state'] == -1:
                            path = './media/books/不完整/' + book_name + '/'
                            for p in os.listdir(path):
                                os.remove(path + p)
                            os.rmdir(path)
                    if os.path.exists('./media/books/简介/' + book_name + '.txt'):
                        os.remove('./media/books/简介/' + book_name + '.txt')
                book.delete()
                books = Book.objects.filter(user_name=user_name)
                i = 1
                for b in books:
                    if os.path.exists('./media/books/完整/' + b.book_name):
                        t = os.listdir('./media/books/完整/' + b.book_name)
                        brief = ''
                        if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                            brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
                        b.download = 1
                        b.book_state = 1
                        b.title = t[0][:-4]
                        b.intro = brief
                        Book.objects.filter(id=b.id).update(download=1, book_state=1, title=t[0][:-4], intro=brief)
                    elif os.path.exists('./media/books/不完整/' + b.book_name):
                        t = os.listdir('./media/books/不完整/' + b.book_name)
                        brief = ''
                        if os.path.exists('./media/books/简介/' + b.book_name + '.txt'):
                            brief = open('./media/books/简介/' + b.book_name + '.txt', encoding='utf-8').read()
                        b.download = 1
                        b.book_state = 0
                        b.title = t[0][:-4]
                        b.intro = brief
                        Book.objects.filter(id=b.id).update(download=1, book_state=-1, title=t[0][:-4], intro=brief)
                    else:
                        b.book_state = -1
                        Book.objects.filter(id=b.id).update(download=0, book_state=-1)
                    b.id = i
                    i += 1
                response["list"] = json.loads(serializers.serialize("json", books))
                response["msg"] = 'success'
                response["error_num"] = 0
                response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
            else:
                response["msg"] = '无此书'
                response["error_num"] = 2
                response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'

    return response


@require_http_methods(["GET", "POST"])
def user_login(request):
    start = time.time()
    response = {}
    try:
        data = json.loads(request.body)
        if cache.get(data.get('name')) == 1:
            response["msg"] = '用户已登录！'
            response["error_num"] = -2
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
        else:
            user = User.objects.filter(name=data.get('name'), password=data.get('password'))
            if user.exists():
                response["msg"] = 'success'
                response["error_num"] = 0
                response["name"] = data.get('name')
                response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
                get_token(request)
                cache.set(data.get('name'), 1, 60 * 5)
            else:
                response["msg"] = "用户不存在或密码错误"
                response["error_num"] = 3
                response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'

    except Exception as e:
        response["msg"] = str(e)
        response["error_num"] = -1
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
def register(request):
    start = time.time()
    response = {}
    try:
        data = json.loads(request.body)
        u = User.objects.filter(name=data.get('name'))
        if u.exists():
            response["msg"] = '用户名已存在'
            response["error_num"] = 4
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
        else:
            user = User(name=data.get('name'), password=data.get('password'))
            user.save()
            get_token(request)
            response["msg"] = 'success'
            response["error_num"] = 0
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'

    except Exception as e:
        response["msg"] = str(e)
        response["error_num"] = -1
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
def upload_image(request):
    start = time.time()
    response = {}
    try:
        if cache.get(request.POST.get('name')) != 1:
            response["msg"] = '登录超时，请重新登录!'
            response["error_num"] = -2
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
            return JsonResponse(response)
        cache.set(request.POST.get('name'), 1, 60 * 5)
        get_token(request)
        if request.method == "POST":
            pic = Pic.objects.filter(pic_name=request.POST.get('name'))
            if pic.exists():
                pic.delete()
                os.remove('./media/images/' + request.POST.get('name') + '.jpg')
            p = Pic(pic_name=request.POST.get('name'), pic_img=request.FILES.get('file'))
            p.save()
            response["msg"] = 'success'
            response["error_num"] = 0
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    except Exception as e:
        response["msg"] = str(e)
        response["error_num"] = -1
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
def upload_text(request):
    start = time.time()
    response = {}
    try:
        if cache.get(request.POST.get('name')) != 1:
            response["msg"] = '登录超时，请重新登录!'
            response["error_num"] = -2
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
            return JsonResponse(response)
        cache.set(request.POST.get('name'), 1, 60 * 5)
        get_token(request)
        if request.method == "POST":
            if os.path.exists('./media/books/上传/' + request.POST.get('name')):
                with open('./media/books/上传/' + request.POST.get('name') + '/' + request.POST.get('book_name') + '.txt', 'w', encoding='utf-8') as f:
                    f.write(str(request.FILES.get('file').read(), encoding='utf-8'))
                f.close()
            else:
                os.mkdir('./media/books/上传/' + request.POST.get('name'))
                with open('./media/books/上传/' + request.POST.get('name') + '/' + request.POST.get('book_name') + '.txt', 'w', encoding='utf-8') as f:
                    f.write(str(request.FILES.get('file').read(), encoding='utf-8'))
                f.close()
            user = User.objects.get(name=request.POST.get('name'))
            b = Book.objects.filter(book_name=request.POST.get('book_name'), user_name=user, is_upload=1)
            if not b.exists():
                book = Book(book_name=request.POST.get('book_name'), user_name=user, is_upload=1, download=1, title=request.POST.get('book_name'), book_state=1, intro='上传的书无简介')
                book.save()
            response["msg"] = 'success'
            response["error_num"] = 0
            response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    except Exception as e:
        response["msg"] = str(e)
        response["error_num"] = -1
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
def logout(request):
    start = time.time()
    response = {}
    try:
        get_token(request)
        data = request.GET
        cache.delete(data.get('name'))
        response["msg"] = '已退出'
        response["error_num"] = 0
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    except Exception as e:
        response["msg"] = str(e)
        response["error_num"] = -1
        response["time"] = str(round((time.time() - start) * 1000, 1)) + 'ms'
    return JsonResponse(response)
