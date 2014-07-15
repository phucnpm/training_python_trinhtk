from django import forms


class SignForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=True, max_length=10)
    guestbook_name = forms.CharField(initial='default_guestbook',
                                     widget=forms.HiddenInput(attrs={'styles': 'display:none;'}))


class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=True, max_length=10)
    guestbook_name = forms.CharField(initial='default_guestbook')
    #id = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    id = forms.CharField(widget=forms.HiddenInput(attrs={'styles': 'display:none;'}))


class ApiForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=True, max_length=10)