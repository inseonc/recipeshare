from django import forms

from .models import Message

#from recipeShareApp.models import *

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('user', 'message', 'photo', )


    def __init__(self, *args, **kwargs):
        #super(PostForm, self).__init__(*args, **kwargs)
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False
        
