from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from accounts.forms import ContactForm, LoginForm, RegisterForm

# all views down below has been transferred to Accounts/View


# def home_page(request):
#     context = {
#         'title': 'Home',
#         'content': 'Welcome to Home Page'
#     }
#     return render(request, 'home_page.html', context)
#
#
# def about_page(request):
#     context = {
#         'title': 'About',
#         'content': 'Welcome to About Page'
#     }
#     return render(request, 'home_page.html', context)
#
#
# def contact_page(request):
#     contact_form = ContactForm(request.POST or None)
#     context = {
#         'title': 'Contact',
#         'content': 'Welcome to Contact Page',
#         'form': contact_form
#     }
#     if contact_form.is_valid():
#         print(contact_form.cleaned_data)

    # if request.method == 'POST':
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    # return render(request, 'contact/view.html', context)


