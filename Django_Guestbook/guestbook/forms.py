from django import  forms
class SignForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=True, max_length=1000000)
    guestbook_name = forms.CharField(initial='default_guestbook')