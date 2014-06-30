from django import  forms
class SignForm(forms.Form):
    guestbook_name = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
