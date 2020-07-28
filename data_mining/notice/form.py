from django import forms
my_choices=(('분야를 선택하세요','분야를 선택하세요'),('언론사','언론사'),('커뮤니티','커뮤니티'),('전체','전체'))


class First(forms.Form):
    field=forms.ChoiceField(choices=my_choices, widget = forms.Select(attrs={'onchange':'submit()'}))

