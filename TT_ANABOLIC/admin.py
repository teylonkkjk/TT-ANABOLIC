from django.contrib import admin
from django.utils.html import format_html
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["get_imagem", "nome", "preco", "quantidade"]
    list_display_links = ["nome"]

   
    def get_imagem(self, obj):
        if obj.imagem:
           
            return format_html(f'<img src="{obj.imagem.url}" style="width: 75px; border-radius: 5px;" />')
        return "sem imagem" 


    get_imagem.short_description = "Imagem"