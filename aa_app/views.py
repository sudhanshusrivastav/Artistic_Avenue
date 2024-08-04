from django.shortcuts import render, redirect, get_object_or_404
from aa_app.models import *
from django.contrib import messages
from django.db.models import Q


#Admin Views

def portal(request):
    if request.method == 'POST':
        pid = request.POST['id']
        password = request.POST['password']
        obj = Portal.objects.filter(pid=pid, password=password)
        if obj:
            request.session['session_key'] = pid
            messages.success(request, 'Logged In')
            return redirect('portal_home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'portal/login.html')
    else:
        return render(request, 'portal/login.html')


def portal_home(request):
    pid = request.session.get('session_key')
    if pid:
        user = Portal.objects.get(pid=pid)
        customer = User.objects.all()
        artist = Artist.objects.all()
        art = Art.objects.all()
        query = Query.objects.all()
        orders = Order.objects.all()
        context = {
            'customer':customer,
            'artist':artist,
            'art':art,
            'query':query,
            'user':user,
            'orders':orders,
        }
        return render(request, 'portal/home.html', context)
    else:
        return redirect('portal')


def uploadpdf(request):
    key = request.session.get('session_key')
    portal = Portal.objects.get(pid=key)
    if portal:
        if request.method =='POST':
            name = request.POST['name']
            desc = request.POST['desc']
            category = request.POST['category']
            link = request.FILES.get('link')
            obj = Pdf()
            obj.name=name
            obj.link = link
            obj.desc=desc
            obj.category = category
            obj.save()
            messages.success(request, 'Pdf Uploaded')
            return redirect('uploadmats')
        else:
            return render(request, 'portal/uploadmats.html', {'user':portal})
    else:
        return redirect('portal')

def uploadvideo(request):
    key = request.session.get('session_key')
    portal = Portal.objects.get(pid=key)
    if portal:
        if request.method =='POST':
            name = request.POST['name']
            desc = request.POST['desc']
            category = request.POST['category']
            link = request.POST['link']
            obj = Video()
            obj.name=name
            obj.link = link
            obj.desc=desc
            obj.category = category
            obj.save()
            messages.success(request, 'Video Uploaded')
            return redirect('uploadmats')
        else:
            return render(request, 'portal/uploadmats.html', {'user':portal})
    else:
        return redirect('portal')


def uploadmats(request):
    key = request.session.get('session_key')
    if key:
        try:
            portal = Portal.objects.get(pid=key)
        except:
            return redirect('portal')
        return render(request, 'portal/uploadmats.html', {'user':portal})
    else:
        return redirect('portal')


def tutorials(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)
    videos = Video.objects.all()
    pdfs= Pdf.objects.all()
    return render(request, 'html/studymats.html', {'videos':videos, 'pdfs':pdfs, 'user':user})


#User Views

def user_register(request):
    if request.method =='POST':
        phone = request.POST['phone']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        pic = request.FILES.get('pic')
        obj = User()
        obj.name=name
        obj.password=password
        obj.email=email
        obj.pic = pic
        obj.phone=phone
        obj.save()
        messages.success(request, 'User Registered Successfully')
        return redirect('user_login')
    else:
        return render(request, 'user/register.html')


def user_login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        obj = User.objects.filter(phone=phone, password=password)
        if obj:
            request.session['session_key'] = phone
            messages.success(request, 'Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'user/login.html')
    else:
        return render(request, 'user/login.html')



def user_chat(request):
    key = request.session.get('session_key')
    user = User.objects.get(phone=key)
    if key:
        user = User.objects.get(phone=key)
        all_messages = Chat.objects.filter(user=user).order_by('artist')
        distinct_users = []
        messages = []
        for message in all_messages:
            if message.artist not in distinct_users:
                distinct_users.append(message.artist)
                messages.append(message)
        
        return render(request, 'user/chat.html', {'msg': messages, 'user':user})
    else:
        return redirect('user_login')



#Artist Views
def artist_register(request):
    if request.method =='POST':
        phone = request.POST['phone']
        category = request.POST['category']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        pic = request.FILES.get('pic')
        obj = Artist()
        obj.name=name
        obj.password=password
        obj.email=email
        obj.pic = pic
        obj.category=category
        obj.phone=phone
        obj.save()
        messages.success(request, 'Artist Registered Successfully')
        return redirect('artist_login')
    else:
        return render(request, 'artist/register.html')


def artist_login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        obj = Artist.objects.filter(phone=phone, password=password)
        if obj:
            request.session['session_key'] = phone
            messages.success(request, 'Logged In')
            return redirect('artist_home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'artist/login.html')
    else:
        return render(request, 'artist/login.html')
    

def artist_home(request):
    key = request.session.get('session_key')
    user = Artist.objects.get(phone=key)
    Oobj = Order.objects.filter(art__artist = user)
    Aobj = Art.objects.filter(artist = user)
    return render(request, 'artist/home.html', {'user':user, 'Oobj':Oobj, 'Aobj':Aobj})



def artists(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)

    obj = Artist.objects.all()
    return render(request, 'html/artists.html', {'obj':obj,'user':user})



def shop(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)
    obj = Art.objects.filter(forsale=True, sold=False)
    return render(request, 'html/shop.html', {'obj':obj,'user':user})


def upload(request):
    key = request.session.get('session_key')
    if request.method =='POST':
        artist = Artist.objects.get(phone=key)
        name = request.POST['name']
        desc = request.POST['desc']
        art_type = request.POST['art_type']
        price = request.POST['price']
        pic = request.FILES.get('pic')
        forsale = request.POST.get('forsale')
        if forsale:
            forsale = True
        else:
            forsale = False
        obj = Art()
        obj.artist = artist
        obj.name=name
        obj.price = price
        obj.art_type=art_type
        obj.desc=desc
        obj.pic = pic
        obj.forsale=forsale
        obj.save()
        messages.success(request, 'Art Uploaded')
        return redirect('artist_home')
    else:
        artist = Artist.objects.get(phone=key)
        return render(request, 'artist/upload.html', {'user':artist})



def add_event(request):
    key = request.session.get('session_key')
    artist=None
    admin=None
    if request.method =='POST':
        try:
            artist = Artist.objects.get(phone=key)
        except:
            admin = Portal.objects.get(pid=key)
            
        
        name = request.POST['name']
        date = request.POST['date']
        venue = request.POST['venue']
        pic = request.FILES.get('pic')
        obj = Event()
        if artist:
            obj.artist = artist
        else:
            obj.admin = admin
        obj.name=name
        obj.date = date
        obj.venue=venue
        obj.pic = pic
        obj.save()
        messages.success(request, 'Art Uploaded')
        return redirect('events')
    else:
        artist=None
        admin=None
        try:
            artist = Artist.objects.get(phone=key)
        except:
            admin = Portal.objects.get(pid=key)
        if artist:
            context = {'user':artist}
        else:
            context = {'user':admin}
        return render(request, 'artist/add_event.html', context)



def artist_messages(request):
    key = request.session.get('session_key')
    artist = Artist.objects.get(phone=key)
    if key:
        artist = Artist.objects.get(phone=key)
        all_messages = Chat.objects.filter(artist=artist).order_by('user')
        distinct_users = []
        messages = []
        for message in all_messages:
            if message.user not in distinct_users:
                distinct_users.append(message.user)
                messages.append(message)
        
        return render(request, 'artist/chat.html', {'msg': messages, 'user':artist})
    else:
        return redirect('artist_login')
    

def send_message(request, id):
    key = request.session.get('session_key')
    user = get_object_or_404(User, id=id)
    artist = Artist.objects.get(phone=key)
    msg = Chat.objects.filter(user=user, artist=artist)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message:
            user = get_object_or_404(User, id=id)
            Chat.objects.create(user=user, artist=artist, artist_message=message)
            return render(request, 'artist/send_message.html', {'msg': msg,'u':user, 'user':artist})
    else:
        return render(request, 'artist/send_message.html', {'msg': msg,'u':user, 'user':artist})


#general

def home(request):
    key = request.session.get('session_key')
    user = None
    artist = Artist.objects.all()
    art = Art.objects.all()
    context = {

            'artist':artist,
            'art':art,
        }
    if key:
        try:
            user = User.objects.get(phone=key)
            return render(request, 'html/home.html', {'user':user, 'artist':artist,'art':art})
        except:
            try:
                user = Artist.objects.get(phone=key)
                return render(request, 'html/home.html', {'user':user, 'artist':artist,'art':art})
            except:
                user = Portal.objects.get(pid=key)
                return render(request, 'html/home.html', {'user':user, 'artist':artist,'art':art})
            
    return render(request, 'html/home.html', context)


def events(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)
    obj = Event.objects.all()
    return render(request, 'html/events.html', {'obj':obj,'user':user})


def gallery(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)
    obj = Art.objects.all()
    return render(request, 'html/gallery.html', {'obj':obj,'user':user})



def billing(request, id):
    key = request.session.get('session_key')
    art = Art.objects.get(id=id)
    if key:
        user = User.objects.get(phone=key)
    else:
        return redirect('user_login')
    
    if request.method == 'POST':
        pic = request.FILES.get('pic')
        order = Order()
        art.sold = True
        order.user = user
        order.art = art
        order.payment = pic
        order.save()
        art.save()
        messages.success(request, 'Order Placed')
        return redirect('user_orders')

    else:
        return render(request, 'user/billing.html',{'art':art})



def artist_orders(request):
    key = request.session.get('session_key')
    user = None
    if key:
        user = Artist.objects.get(phone=key)
        obj = Order.objects.filter(art__artist = user)
        return render(request, 'artist/orders.html', {'obj':obj,'user':user})
    else:
        return redirect('artist_login')



def portal_orders(request):
    key = request.session.get('session_key')
    if key:
        user = Portal.objects.get(pid=key)
        orders = Order.objects.all()
        if request.method == 'POST':
            order_id = request.POST.get('order_id')
            status = request.POST.get('status')
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return redirect('portal_orders')
        else:
            return render(request, 'portal/orders.html', {'orders': orders, 'user': user})
    else:
        return redirect('portal')



def user_orders(request):
    key = request.session.get('session_key')
    user = None
    if key:
        user = User.objects.get(phone=key)
        obj = Order.objects.filter(user = user)
        return render(request, 'user/orders.html', {'obj':obj,'user':user})
    else:
        return redirect('user_login')



def chat(request, id):
    key = request.session.get('session_key')
    if key:
        try:
            user = User.objects.get(phone=key)
        except User.DoesNotExist:

            try:
                user = Artist.objects.get(phone=key)
            except Artist.DoesNotExist:
                user = Portal.objects.get(pid=key)

        receiver = get_object_or_404(Artist, id=id)

        if request.method == 'POST':

            message = request.POST.get('message', '')
            if message:
                chat_message = Chat()
                chat_message.user = user
                chat_message.artist = receiver
                if isinstance(user, User):
                    chat_message.user_message = message
                elif isinstance(user, Artist):
                    chat_message.artist_message = message
                chat_message.save()
                return redirect('chat', id=id)
        else:

            chat_messages = Chat.objects.filter(user=user, artist=receiver)
            return render(request, 'html/chat.html', {'user': user, 'receiver': receiver, 'chat_messages': chat_messages})
    return redirect('user_login')


def show_art(request, phone):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)
    artist_obj = Artist.objects.get(phone=phone)
    obj = Art.objects.filter(artist = artist_obj)
    return render(request, 'html/gallery.html', {'obj':obj,'user':user})



def query(request):
    key = request.session.get('session_key')
    user = None
    if key:
        try:
            user = User.objects.get(phone=key)
        except:
            try:
                user = Artist.objects.get(phone=key)
            except:
                user = Portal.objects.get(pid=key)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        query = request.POST['query']
        obj = Query()
        obj.name = name
        obj.email = email
        obj.question = query
        obj.save()
        messages.success(request, 'Query Submitted')
        return redirect('home')
    else:
        return render(request, 'html/query.html', {'user':user})



def logout(request):
    request.session.flush()
    return redirect('home')