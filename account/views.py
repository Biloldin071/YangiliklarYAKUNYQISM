from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .form import UserRegistrationForm, UserEditForm, ProfilEditForm

from .models import Profil


def profil_view(request):
    user = request.user
    profil = Profil.objects.get(user=user)
    context = {
        'user': user,
        'profil': profil
    }

    return render(request, 'pages/user_profil.html', context)





class SignUpView2(View):

    def get(self, request):
        user_form = UserRegistrationForm()
        # print(user_form)
        context = {
            "user_form": user_form
        }
        return render(request, 'account/register.html', {"user_form": user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.data.get("username"):
            pass

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            context = {
                "new_user": new_user
            }
            return render(request, 'account/register_done.html', context)


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profil_form = ProfilEditForm(instance=request.user.profil,
                                     data=request.POST,
                                     files=request.FILES)
        if user_form.is_valid() and profil_form.is_valid():
            user_form.save()
            profil_form.save()
            return redirect('user_profil')

    else:
        user_form = UserEditForm(instance=request.user)
        profil_form = ProfilEditForm(instance=request.user.profil)

    return render(request, 'account/profil_edit.html', {"user_form": user_form, 'profil_form': profil_form})


class EditUserView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profil_form = ProfilEditForm(instance=request.user.profil)
        return render(request, 'account/profil_edit.html', {"user_form": user_form, 'profil_form': profil_form})

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profil_form = ProfilEditForm(instance=request.user.profil,
                                     data=request.POST,
                                     files=request.FILES)
        if user_form.is_valid() and profil_form.is_valid():
            user_form.save()
            profil_form.save()
            return redirect('user_profil')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': users
    }
    return render(request, template_name='pages/admin_page.html', context=context)
