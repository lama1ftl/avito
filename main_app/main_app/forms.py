from django import forms



class LoginForm(forms.Form):
    login = forms.CharField(label='login')
    pwd = forms.CharField(label='pwd')


class RegForm(forms.Form):
    login = forms.CharField(label='login')
    pwd = forms.CharField(label='pwd')
    pwd2 = forms.CharField(label='pwd2')
    email = forms.EmailField(label='email')
    name = forms.CharField(label='name')
    role = forms.CharField(label='role')
    phone = forms.CharField(label='phone')
    city = forms.CharField(label='city')


class AddItemForm(forms.Form):
    name = forms.CharField(label='name')
    price = forms.CharField(label='price')
    category = forms.ChoiceField(label='category', choices=(('cat1', 'cat1'),
                                                            ('cat2', 'cat2')))
    text = forms.CharField(label='text')
    status = forms.ChoiceField(label='status', choices=(('yes', 'yes'),
                                                        ('no', 'no')))

    image = forms.FileField(required=False, label='images',
                            widget=forms.ClearableFileInput(
                                attrs={'multiple': True}))


class SearchForm(forms.Form):
    search_text = forms.CharField(label='search_text')
    category = forms.ChoiceField(label='category', choices=(('cat1', 'cat1'),
                                                            ('cat2', 'cat2')))


class RedactForm(forms.Form):
    email = forms.EmailField(label='email')
    name = forms.CharField(label='name')
    surname = forms.CharField(label='surname')
    city = forms.CharField(label='city')
    phone = forms.CharField(label='phone')




