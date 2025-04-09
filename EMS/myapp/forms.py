from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "email", "department", "role"]  # Remove non-existing fields


from django import forms
from .models import Message
from django.contrib.auth import get_user_model  # Correct way to get the user model

User = get_user_model()  # This will correctly use 'myapp.CustomUser'

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Now using CustomUser model
        label="Send To",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body']  # ✅ Ensure only title and body are included
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }



from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']  # Adjust fields according to your model
    
    # Add any additional custom validation or logic here if necessary

