from django import forms
from .models import Teacher, Enrollment


class CourseForm(forms.Form):
    name = forms.CharField(label='課名', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    code = forms.CharField(label='課號', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    teacher = forms.ModelChoiceField(
        label='任課老師 (從下拉選擇)',
        queryset=Teacher.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    new_teacher = forms.CharField(
        label='新增老師 (若要新增，請填此欄，會優先使用此欄)',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['midterm_score', 'final_score']
        widgets = {
            'midterm_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'final_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'})
        }
        labels = {
            'midterm_score': '期中分數',
            'final_score': '期末分數'
        }
