from datetime import time
from django.http import Http404
from django.utils import timezone
from collections import OrderedDict
from django.contrib import messages
from django.contrib.auth.models import User
from main.models import Appointment, Employee, Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,  login, logout
from django.shortcuts import get_object_or_404, render, redirect
from main.google_calender_api import calender_api, confirmation, getCreds
from main.forms import AppointmentForm, EditPostForm, SignUpForm, PostForm

# Create your views here.


def add_times(t1, t2):
    hours = t1.hour + t2.hour
    minutes = t1.minute + t2.minute
    hours += minutes // 60
    minutes %= 60
    new_time = time(hour=hours, minute=minutes)
    return new_time


def home(request):
    request.session['event'] = None
    request.session['doctor_id'] = None
    request.session['confirm_link'] = None
    if request.user.is_authenticated:
        messages.success(request, "You are already signed in!")
        if request.user.employee.designation == "Doctor":
            return redirect('doctor-dashboard')
        else:
            return redirect('patient-dashboard')
    return render(request, 'home.html')


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Signed Out Successfully!")
        return redirect('home')
    else:
        raise Http404


def doctorSignin(request):
    context = {
        "title": "Doctor's",
        "name": "doctor",
    }
    if request.user.is_authenticated:
        if request.user.employee.designation == "Doctor":
            messages.success(request, "You are already signed in!")
            return redirect('doctor-dashboard')
        else:
            messages.error(
                request, 'Sign out to access this page!')
            return redirect('patient-dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.employee.designation == "Doctor":
                    login(request, user)
                    messages.success(
                        request, "You have successfully signed in!")
                    return redirect('doctor-dashboard')
                else:
                    messages.error(request, "Invalid Credentials! Try Again!")
                    return render(request, 'signin.html', context)
            else:
                messages.error(request, "Invalid Credentials! Try Again!")
                return render(request, 'signin.html', context)
        else:
            return render(request, 'signin.html', context)


def doctorSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            profile_pic = form.cleaned_data['profile_picture']
            usrname = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pswd = form.cleaned_data['password']
            cpswd = form.cleaned_data['confirm_password']
            addrln = form.cleaned_data['address_line_1']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pin = form.cleaned_data['pin_code']
            if User.objects.filter(username=usrname).exists():
                form.add_error(
                    None, "Username already exists, try another!")
            else:
                if pswd == cpswd:
                    user = User.objects.create_user(usrname, email, pswd)
                    user.first_name = fname.capitalize()
                    user.last_name = lname.capitalize()
                    user.save()
                    user_details = Employee(user=user,
                                            designation="Doctor",
                                            address_line_1=addrln,
                                            city=city,
                                            state=state,
                                            pin_code=pin,
                                            profile_picture=profile_pic)
                    user_details.save()
                    messages.success(
                        request, "Your account has been successfully created!")
                    return doctorSignin(request)
                else:
                    form.add_error(None, "Passwords doesn't match!")
    else:
        form = SignUpForm()

    context = {
        "title": "Doctor's",
        "name": "doctor",
        "form": form,
    }
    return render(request, 'signup.html', context)


@login_required(login_url='/doctor-signin')
def doctorDashboard(request):
    user = request.user
    if user.employee.designation == "Doctor":
        context = {
            "title": "Doctor's",
            "name": "doctor",
            "fname": user.first_name,
            "lname": user.last_name,
            "profile_pic": str(user.employee.profile_picture),
            "username": user.username,
            "email": user.email,
            "addrln": user.employee.address_line_1,
            "city": user.employee.city,
            "state": user.employee.state,
            "pin": user.employee.pin_code,

        }
        return render(request, 'dashboard.html', context)
    else:
        raise Http404


def patientSignin(request):
    context = {
        "title": "Patient's",
        "name": "patient",
    }
    if request.user.is_authenticated:
        if request.user.employee.designation == "Patient":
            messages.success(request, "You are already signed in!")
            return redirect('patient-dashboard')
        else:
            messages.error(
                request, 'Sign out to access this page!')
            return redirect('doctor-dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.employee.designation == "Patient":
                    login(request, user)
                    messages.success(
                        request, "You have successfully signed in!")
                    return redirect('patient-dashboard')
                else:
                    messages.error(request, "Invalid Credentials! Try Again!")
                    return render(request, 'signin.html', context)
            else:
                messages.error(request, "Invalid Credentials! Try Again!")
                return render(request, 'signin.html', context)
        else:
            return render(request, 'signin.html', context)


def patientSignup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            profile_pic = form.cleaned_data['profile_picture']
            usrname = form.cleaned_data['username']
            email = form.cleaned_data['email']
            pswd = form.cleaned_data['password']
            cpswd = form.cleaned_data['confirm_password']
            addrln = form.cleaned_data['address_line_1']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pin = form.cleaned_data['pin_code']
            if User.objects.filter(username=usrname).exists():
                form.add_error(
                    None, "Username already exists, try another!")
            else:
                if pswd == cpswd:
                    user = User.objects.create_user(usrname, email, pswd)
                    user.first_name = fname.capitalize()
                    user.last_name = lname.capitalize()
                    user.save()
                    user_details = Employee(user=user,
                                            designation="Patient",
                                            address_line_1=addrln,
                                            city=city,
                                            state=state,
                                            pin_code=pin,
                                            profile_picture=profile_pic)
                    user_details.save()
                    messages.success(
                        request, "Your account has been successfully created!")
                    return patientSignin(request)
                else:
                    form.add_error(None, "Passwords doesn't match!")
    else:
        form = SignUpForm()

    context = {
        "title": "Patient's",
        "name": "patient",
        "form": form,
    }
    return render(request, 'signup.html', context)


@login_required(login_url='/patient-signin')
def patientDashboard(request):
    user = request.user
    if user.employee.designation == "Patient":
        context = {
            "title": "Patient's",
            "name": "patient",
            "fname": user.first_name,
            "lname": user.last_name,
            "profile_pic": str(user.employee.profile_picture),
            "username": user.username,
            "email": user.email,
            "addrln": user.employee.address_line_1,
            "city": user.employee.city,
            "state": user.employee.state,
            "pin": user.employee.pin_code,

        }
        return render(request, 'dashboard.html', context)
    else:
        raise Http404


@login_required(login_url='/doctor-signin')
def createPost(request):
    if request.user.employee.designation == 'Doctor':
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                category = form.cleaned_data['category']
                summary = form.cleaned_data['summary']
                content = form.cleaned_data['content']
                image = form.cleaned_data['image']
                draft = form.cleaned_data['draft']
                date = timezone.now()
                post = Post(
                    title=title,
                    author=request.user,
                    category=category,
                    summary=summary,
                    content=content,
                    image=image,
                    draft=draft,
                    date=date
                )
                post.save()
                messages.success(request, "Post Created Successfully!")
            return redirect('doctor-dashboard')

        else:
            form = PostForm()

        context = {
            "form": form,
        }

        return render(request, 'create-post.html', context)
    else:
        raise Http404


@login_required(login_url='/doctor-signin')
def editPost(request, slug):
    from django.forms.models import model_to_dict
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            draft = form.cleaned_data['draft']
            image = form.cleaned_data['image']
            summary = form.cleaned_data['summary']
            content = form.cleaned_data['content']
            date = timezone.now()

            if image is not None:
                post.image = image

            post.title = title
            post.category = category
            post.draft = draft
            post.summary = summary
            post.content = content
            post.date = date
            post.save()
            messages.success(request, "Post Updated Successfully!")
            return redirect('doctor-dashboard')
    else:
        form = EditPostForm(initial=model_to_dict(post))
    context = {
        'form': form,
        'id': post.id,
        'slug': post.slug
    }
    return render(request, 'edit-post.html', context)


@login_required(login_url='/doctor-signin')
def deletePost(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    post.delete()
    messages.success(request, "Post Deleted Successfully!")
    return redirect('doctor-dashboard')


@login_required(login_url='/doctor-signin')
def drafts(request):
    if request.user.employee.designation == 'Doctor':
        posts = []
        categories_dict = Post.objects.values(
            'category').order_by('-date', '-id')

        if not categories_dict:
            return render(request, 'drafts.html', {'posts': posts})

        for _ in categories_dict:
            categories = [item['category'] for item in categories_dict]
        categories = list(OrderedDict.fromkeys(categories))

        for category in categories:
            post = Post.objects.filter(
                author=request.user, category=category, draft=True).order_by('-date', '-id')
            if post:
                posts.append([post, category])
        context = {
            'posts': posts
        }
        return render(request, 'drafts.html', context)
    else:
        raise Http404


@login_required(login_url='/doctor-signin')
def myPosts(request):
    if request.user.employee.designation == 'Doctor':
        posts = []
        categories_dict = Post.objects.values(
            'category').order_by('-date', '-id')
        if not categories_dict:
            return render(request, 'my-posts.html', {'posts': posts})

        for _ in categories_dict:
            categories = [item['category'] for item in categories_dict]
        categories = list(OrderedDict.fromkeys(categories))
        for category in categories:
            post = Post.objects.filter(
                author=request.user, category=category, draft=False).order_by('-date', '-id')
            if post:
                posts.append([post, category])
        context = {
            'posts': posts
        }
        return render(request, 'my-posts.html', context)
    else:
        raise Http404


@login_required(login_url='/patient-signin')
def bookAppointment(request):
    if request.user.employee.designation == "Patient":
        doctors = Employee.objects.filter(designation='Doctor')
        if request.method == 'GET':
            request.session['doctor_id'] = None

        if (request.method == 'POST') and ('btn-doctor' in request.POST) and (request.session['doctor_id'] is None):
            request.session['doctor_id'] = request.POST.get('btn-doctor')

        if (request.method == 'POST') and ('btn-doctor' not in request.POST) and (request.session['doctor_id'] is not None):
            form = AppointmentForm(request.POST)
            if form.is_valid():
                speciality = form.cleaned_data['required_speciality']
                date = form.cleaned_data['date']
                start_time = form.cleaned_data['start_time']
                end_time = add_times(start_time, time(minute=45))
                if speciality != "Default":
                    appointment = Appointment(user=request.user,
                                              doctor=User.objects.get(
                                                  id=request.session['doctor_id']),
                                              required_speciality=speciality,
                                              date=date,
                                              start_time=start_time,
                                              end_time=end_time)
                    appointment.save()
                    auth = confirmation()
                    request.session['confirm_link'] = auth[0]
                    request.session['state'] = auth[1]
                    return redirect(auth[0])
                else:
                    form.add_error('required_speciality',
                                   'Please select a speciality.')
        else:
            form = AppointmentForm()

        context = {
            'form': form,
            'doctors': doctors,
            'doctor_id': request.session['doctor_id']
        }
        return render(request, 'book-appointment.html', context)

    else:
        raise Http404


@login_required(login_url='/patient-signin')
def confirm(request):
    if request.user.employee.designation == "Patient":
        state = request.GET.get('state')
        code = request.GET.get('code')
        scope = request.GET.get('scope')
        url = f"https://127.0.0.1:8000/confirm?state={state}&code={code}&scope={scope}"
        creds = getCreds(request.session['state'], url)
        appointment = Appointment.objects.filter(
            user=request.user).order_by('-id')[0]
        date = appointment.date.strftime('%Y-%m-%d')
        start = f"{date}T{appointment.start_time.strftime('%H:%M:%S')}+05:30"
        end = f"{date}T{appointment.end_time.strftime('%H:%M:%S')}+05:30"
        event = calender_api(
            creds=creds,
            patient=f"{appointment.user.first_name} {appointment.user.last_name}",
            speciality=appointment.required_speciality,
            start=start,
            end=end,
            doctorEmail=appointment.doctor.email)
        request.session['event'] = event
        messages.success(
            request, "Your appointment has been successfully booked!")
        return redirect('appointment-details')
    else:
        Http404


@ login_required(login_url='/patient-signin')
def appointmentDetails(request):
    if request.user.employee.designation == "Patient":
        appointment = Appointment.objects.filter(
            user=request.user).order_by('-id')[0]
        date = appointment.date.strftime('%Y-%m-%d')
        context = {
            "doctor": appointment.doctor,
            "required_speciality": appointment.required_speciality,
            "date": date,
            "start_time": appointment.start_time.strftime('%H:%M'),
            "end_time": appointment.end_time.strftime('%H:%M'),
            "event": request.session['event']
        }
        return render(request, 'appointment-details.html', context)
    else:
        raise Http404


def postDetail(request, slug):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, slug=slug)
        if post.draft == True:
            raise Http404
        return render(request, 'post-detail.html', {'post': post})
    else:
        messages.error(request, "To access this page, you must be logged in!")
        return redirect('home')


def blog(request):
    if request.user.is_authenticated:
        posts = []
        categories_dict = Post.objects.values(
            'category').order_by('-date', '-id')
        if not categories_dict:
            return render(request, 'blog.html', {'posts': posts})

        for _ in categories_dict:
            categories = [item['category'] for item in categories_dict]
        categories = list(OrderedDict.fromkeys(categories))
        for category in categories:
            post = Post.objects.filter(
                category=category, draft=False).order_by('-date', '-id')
            if post:
                posts.append([post, category])
        context = {
            'posts': posts
        }
        print(posts)
        return render(request, 'blog.html', context)
    else:
        messages.error(request, "To access this page, you must be logged in!")
        return redirect('home')
