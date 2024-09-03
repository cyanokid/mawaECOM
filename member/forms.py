from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile

#To add field in UserCreationForm
class UserInfoForm(forms.ModelForm):
   
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Phone'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Address 1'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Address 2'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'City'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Zipcode'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Country'}), required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'zipcode', 'country')

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
    
    def __init__(self, *args, **kwargs):
	    super(ChangePasswordForm, self).__init__(*args, **kwargs)

	    self.fields['new_password1'].widget.attrs['class'] = 'form-control'
	    self.fields['new_password2'].widget.attrs['class'] = 'form-control'


class RegisterUserForm(UserCreationForm):
    #widget are used to apply boostrap
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    #yang ni kita tambah sebab tiada pada field yang kita tambah.
    #yang ni object yang dah built in, jadi tinggal tambah widgetnya sahaja.
    def __init__(self, *args, **kwargs):
	    super(RegisterUserForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    self.fields['password1'].widget.attrs['class'] = 'form-control'
	    self.fields['password2'].widget.attrs['class'] = 'form-control'

class UpdateUserForm(UserChangeForm):
    #Hide Password stuff
    password = None
    #widget are used to apply boostrap
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    #yang ni kita tambah sebab tiada pada field yang kita tambah.
    #yang ni object yang dah built in, jadi tinggal tambah widgetnya sahaja.
    def __init__(self, *args, **kwargs):
	    super(UpdateUserForm, self).__init__(*args, **kwargs)

	    self.fields['username'].widget.attrs['class'] = 'form-control'
	    

