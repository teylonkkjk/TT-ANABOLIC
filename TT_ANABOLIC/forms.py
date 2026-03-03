

from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Nome do Produto'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Descreva o produto...',
                'rows': 4
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': '99.90'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Quantidade em estoque'
            }),
            'imagem': forms.FileInput(attrs={
                'class': 'w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-yellow-400'
            })
        }

from django import forms
from .models import Endereco, Produto
tailwind_classes = (
    'bg-gray-900 border-2 border-gray-700 text-blue-400 text-base rounded-lg '
    'focus:ring-blue-500 focus:border-blue-500 block w-full p-3 '
    'placeholder-gray-500'
)

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        exclude = ['usuario']
        widgets = {
            'cep': forms.TextInput(attrs={'class': tailwind_classes, 'placeholder': '00000-000'}),
            'logradouro': forms.TextInput(attrs={'class': tailwind_classes, 'placeholder': 'Nome da Rua ou Avenida'}),
            'numero': forms.TextInput(attrs={'class': tailwind_classes, 'placeholder': 'Nº'}),
            'bairro': forms.TextInput(attrs={'class': tailwind_classes, 'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'class': tailwind_classes, 'placeholder': 'Sua cidade'}),
            'estado': forms.TextInput(attrs={'class': tailwind_classes}),
        }
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ['usuario']
        widgets = {
            'nome': forms.TextInput(attrs={'class': tailwind_classes, 'placeholder': 'Nome do Produto'}),
            'descricao': forms.Textarea(attrs={'class': tailwind_classes, 'placeholder': 'Descreva o produto...'}),
            'preco': forms.NumberInput(attrs={'class': tailwind_classes, 'placeholder': '99.90'}),
            'quantidade': forms.NumberInput(attrs={'class': tailwind_classes, 'placeholder': 'Quantidade em estoque'}),
            'imagem': forms.FileInput(attrs={'class': tailwind_classes}),
        }
