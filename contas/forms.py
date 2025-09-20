from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import ResellerUser
from .managers import ResellerUserManager

class LoginForm(forms.Form):
    email_or_phone = forms.CharField(label='E-mail ou Telefone')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        ident = data.get('email_or_phone', '').strip()
        pwd = data.get('password')
        user = None
        if '@' in ident:
            user = ResellerUser.objects.filter(email__iexact=ident).first()
        else:
            ident_norm = ResellerUserManager._clean_phone(ident)
            user = ResellerUser.objects.filter(phone=ident_norm).first()

        if not user or not check_password(pwd, user.password):
            raise forms.ValidationError('Credenciais inválidas.')
        if not user.is_active:
            raise forms.ValidationError('Conta desativada.')
        data['user'] = user
        return data

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': '••••••••',
        }),
        label='Senha',
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': '••••••••',
        }),
        label='Confirme a senha',
    )

    class Meta:
        model = ResellerUser
        fields = ('email', 'phone', 'full_name', 'cupom_reseller')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'seu@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': '(11) 99999-9999',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Seu nome completo',
            }),
            'cupom_reseller': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'CUPOM do revendedor',
            }),
        }

    def clean(self):
        data = super().clean()
        if not data.get('email') and not data.get('phone'):
            raise forms.ValidationError('Informe e-mail ou telefone.')
        if data.get('password') != data.get('password_confirm'):
            raise forms.ValidationError('Senhas não conferem.')
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante a classe Bulma 'input' em todos os campos (caso algum widget seja sobrescrito)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            classes = set(filter(None, css.split(' ')))
            classes.add('input')
            field.widget.attrs['class'] = ' '.join(sorted(classes))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user