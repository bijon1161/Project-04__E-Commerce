from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import ContactForm, LoginForm, RegisterForm, GuestForm
from .models import Guest
from .signals import user_logged_in


def home_page(request):
    context = {
        'title': 'Home',
        'content': 'Welcome to Home Page'
    }
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        'title': 'About',
        'content': 'Welcome to About Page'
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'title': 'Contact',
        'content': 'Welcome to Contact Page',
        'form': contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({'message': 'Thank You for your Submission!'})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('fullname'))
    return render(request, 'contact/view.html', context)


def guest_register(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form,
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    next_post = '/cart/checkout' # shudnt be this way
    redirect_path = next_ or next_post or None
    print(redirect_path)
    if form.is_valid():
        email       = form.cleaned_data.get('email')
        new_guest = Guest.objects.create(email=email)
        print(new_guest)
        print(new_guest.email)
        request.session['guest_id'] = new_guest.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register')

    return redirect('/register')


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        next_post = '/cart/checkout'  # shudnt be this way
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')

        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {
#         'form': form,
#         'title': 'Login'
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     next_post = '/cart/checkout' #shudnt be this way
#     redirect_path = next_ or next_post or None
#     print(redirect_path)
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('/')
#         else:
#             print('Error!')
#
#     return render(request, 'accounts/login.html', context)



# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {
#         'form': form,
#         'title': 'Register'
#     }
#     if form.is_valid():
#         # print(form.cleaned_data)
#         # username = form.cleaned_data.get('username')
#         # email = form.cleaned_data.get('email')
#         # password = form.cleaned_data.get('password')
#         # new_user = User.objects.create_user(username, email, password)
#         # print(new_user)
#         form.save()
#     return render(request, 'accounts/register.html', context)
