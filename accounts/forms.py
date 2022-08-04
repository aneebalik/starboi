from django import forms
from .models import Account,UserProfile
from dataclasses import field,fields




class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password'
    })) 

    class Meta:
        model   = Account
        fields  = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'profile_image']


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password     = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields= ['first_name','last_name','phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args,**kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields= ['address_line_1','address_line_2','city','state','country','profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs) 
        for field in self.fields:
            self.fields[field].widget.attrs['class'] ='form-control'


# class AccountUpdateForm(forms.ModelForm):

#     class Meta:
#         model = Account
#         fields = ['username', 'email', 'profile_picture', 'hide_email','address_line_1','address_line_2','city','state','country' ]

#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         try:
#             account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
#         except Account.DoesNotExist:
#             return email
#         raise forms.ValidationError('Email "%s" is already in use.' % account)

#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#             account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
#         except Account.DoesNotExist:
#             return username
#         raise forms.ValidationError('Username "%s" is already in use.' % username)


#     def save(self, commit=True):
#         account = super(AccountUpdateForm, self).save(commit=False)
#         account.username        = self.cleaned_data['username']
#         account.email           = self.cleaned_data['email'].lower()
#         account.profile_picture = self.cleaned_data['profile_picture']
#         account.hide_email      = self.cleaned_data['hide_email']
#         account.address_line_1  = self.cleaned_data['hide_email']
#         account.address_line_2  = self.cleaned_data['hide_email']
#         account.city            = self.cleaned_data['hide_email']
#         account.state           = self.cleaned_data['hide_email']
#         account.country         = self.cleaned_data['hide_email']
#         if commit:
#             account.save()
#         return account