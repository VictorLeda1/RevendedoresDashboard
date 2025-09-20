from django import forms
from .models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = (
            'produto',
            'valor',
            'cliente',
            'vendedor',
            'cupom',
        )
        widgets = {
            'produto': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Nome do produto'}),
            'valor': forms.NumberInput(attrs={'class': 'input', 'step': '0.01', 'placeholder': '0,00'}),
            'cliente': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Cliente (opcional)'}),
            'vendedor': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Vendedor (opcional)'}),
            'cupom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Cupom (opcional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante a classe Bulma 'input' em todos os campos
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            classes = set(filter(None, css.split(' ')))
            classes.add('input')
            field.widget.attrs['class'] = ' '.join(sorted(classes))
