from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm, BaseSignupForm
from allauth.account.utils import setup_user_email
from django import forms
from django.http import HttpResponse

from .models import PetProfile, GENDER_TYPE


class ProfileForm(forms.Form):
    user_telephone = forms.CharField(max_length=50, label='联系方式', required=False)

    pet_name = forms.CharField(max_length=50, label='宠物姓名', required=False)
    pet_age = forms.IntegerField(label='宠物年龄', required=False)
    pet_id = forms.IntegerField(label='宠物编号', required=False)
    pet_breed = forms.CharField(max_length=50, label='宠物种类', required=False)
    pet_gender = forms.ChoiceField(choices=GENDER_TYPE, label='宠物性别', required=False)

    class Meta:
        model = PetProfile
        fields = ['username', 'password', 'pet_gender', 'pet_breed', 'pet_id', 'pet_age', 'email', 'phone', 'pet_name']


# 重写注册表单，注册的时候创建关联对象,要先继承原来的类
class CustomSignupForm(ProfileForm, SignupForm):
    # user_telephone = forms.CharField(max_length=50, label='联系方式', required=False)
    #
    # pet_name = forms.CharField(max_length=50, label='宠物姓名', required=False)
    # pet_age = forms.IntegerField(label='宠物年龄', required=False)
    # pet_id = forms.IntegerField(label='宠物编号', required=False)
    # pet_breed = forms.CharField(max_length=50, label='宠物种类', required=False)
    # pet_gender = forms.ChoiceField(choices=GENDER_TYPE, label='宠物性别', required=False)

    # 对某方法进行重写，注意名字
    def custom_signup(self, request, user):
        print(request.POST)
        print("-----------------------")
        user_profile = PetProfile()
        user_profile.user = user
        user_profile.user_telephone = request.POST['user_telephone']
        user_profile.pet_name = request.POST['pet_name']
        user_profile.pet_age = request.POST['pet_age']
        user_profile.pet_id = request.POST['pet_id']
        user_profile.pet_breed = request.POST['pet_breed']
        user_profile.pet_gender = request.POST['pet_gender']
        user.save()
        user_profile.save()


# 重写重置密码表单
class CustomResetPasswordForm(forms.Form):
    """
    重置密码表单,要求验证手机号码
    """
    user_telephone = forms.CharField(
        label='电话号码',
        max_length=18,
        required=True)

    def clean_identity_card(self):
        # 取到身份证号码
        user_telephone = self.cleaned_data["user_telephone"]
        print("clean_identity_card" + user_telephone)
        # 在PetProfile中筛选符合条件的用户，返回用户名
        # 如果用get方法的话取不到会直接报错，所以用filter方法
        # 同样的，身份证需要设置UNIQUE
        username = PetProfile.objects.filter(
            user_telephone=user_telephone)
        if not username:
            raise forms.ValidationError(
                "电话号码不存在"
            )
        return self.cleaned_data["user_telephone"]

    def save(self, request, **kwargs):
        # print(self.cleaned_data['user_telephone'])# str
        # print("----------------------------")
        # print(request.POST)
        return self.cleaned_data['user_telephone']
