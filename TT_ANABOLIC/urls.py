from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('adicionar_carrinho/<int:id>', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/', views.carrinho_view, name='carrinho'), 
    path('remover_do_carrinho/<int:id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('cadastrar-produto/', views.cadastrar_produto_view, name='cadastrar_produto'),
    path('editar_produto/<int:id>/', views.editar_produto_view, name='editar_produto'),
    path('remover_produto/<int:id>/', views.remover_produto_view, name='remover_produto'),
    path('aumentar-quantidade/<int:item_id>/', views.aumentar_quantidade, name='aumentar_quantidade'),
    path('diminuir-quantidade/<int:item_id>/', views.diminuir_quantidade, name='diminuir_quantidade'),
    path('perfil/', views.ver_perfil, name='perfil'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
    path('gerenciamento/usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('gerenciamento/usuarios/admin/<int:user_id>/', views.gerenciar_admin, name='gerenciar_admin'),
    path('carrinho/limpar/', views.limpar_carrinho, name='limpar_carrinho'),
    path('admin/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('perfil/endereco/', views.perfil_endereco, name='perfil_endereco'),
    path('checkout/endereco/', views.checkout_endereco, name='checkout_endereco'),
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)