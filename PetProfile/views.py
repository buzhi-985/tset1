from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from allauth.account.views import PasswordResetView, PasswordResetFromKeyView, AjaxCapableProcessFormViewMixin
from allauth.utils import build_absolute_uri
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomSignupForm, CustomResetPasswordForm, ProfileForm
from .models import PetProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})


@login_required
def profile_update(request):
    user = request.user
    # print(user)
    user_profile = get_object_or_404(PetProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            user_profile.user_telephone = form.cleaned_data['user_telephone']
            user_profile.pet_name = form.cleaned_data['pet_name']
            user_profile.pet_age = form.cleaned_data['pet_age']
            user_profile.pet_id = form.cleaned_data['pet_id']
            user_profile.pet_breed = form.cleaned_data['pet_breed']
            user_profile.pet_gender = form.cleaned_data['pet_gender']

            user_profile.save()

            return HttpResponseRedirect(reverse('PetProfile:profile'))

    else:
        default_data = {'user_telephone': user_profile.user_telephone,
                        'pet_name': user_profile.pet_name,
                        'pet_age': user_profile.pet_age,
                        'pet_id': user_profile.pet_id,
                        'pet_breed': user_profile.pet_breed,
                        'pet_gender': user_profile.pet_gender,
                        }
        form = ProfileForm(default_data)

    return render(request, 'account/profile_update.html', {'form': form, 'user': user})

def bb(request):
    return render(request,'account/nav.html')

class CustomPasswordResetView(PasswordResetView):

    def get(self, request, *args, **kwargs):
        return render(request, 'account/password_reset.html', {'form': CustomResetPasswordForm})

    def post(self, request, *args, **kwargs):
        # print(request.POST)

        reset_password_form = CustomResetPasswordForm(request.POST)
        # print(reset_password_form)
        if reset_password_form.is_valid():
            # 取到身份证之后取到用户对象
            user_telephone = reset_password_form.clean_identity_card()
            # username = PetProfile.objects.get(user_telephone=user_telephone).first()
            username = PetProfile.objects.filter(user_telephone=user_telephone).first() # 因为没设置手机号码唯一只能通过这解决
            # print(username)
            user = User.objects.filter(username=username).first()
            # print(user, username)
            # 生成token
            token_generator = kwargs.get("token_generator", default_token_generator)
            temp_key = token_generator.make_token(user)
            # print(temp_key)
            path = reverse(
                "account_reset_password_from_key",
                kwargs=dict(uidb36=user_pk_to_url_str(user), key=temp_key),
            )
            url = build_absolute_uri(request, path)
            # 重定向至修改密码链接
            return redirect(url)
        else:
            return render(request, 'account/identity_card_error.html')
