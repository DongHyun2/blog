from django import forms
from .models import Blog

# class BlogPost(forms.ModelForm): #모델을 기반으로한 입력공간을 만들기 위해선
#   class Meta:
#        model = Blog #어떤모델
#        fields = ['title', 'body'] #어떤 것을 입력받을지 >> 처리해주는 함수를 views.py에

class BlogPost(forms.Form):
    email = forms.EmailField()
    files = forms.FileField()
    url = forms.URLField()
    words = forms.CharField(max_length=200)
    max_number = forms.ChoiceField(choices=[('1','one'),('2','two')])