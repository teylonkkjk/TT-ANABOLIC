from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, authenticate, login 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from TT_ANABOLIC.models import ItemPedido, Produto, Usuario, Carrinho, ItensCarrinho, Pedido, Endereco
from django.contrib.auth.models import User, Group, Permission
from .forms import ProdutoForm, EnderecoForm
from rolepermissions.decorators import has_permission_decorator
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome') 
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        data_nascimento = request.POST.get('data_nascimento')
        user = User.objects.filter(email=email).exists()
        if user:
            messages.error(request, 'Usuário já cadastrado')
            return redirect('login')
        user = User.objects.create_user(email=email, username=email, first_name=nome)
        user.set_password(senha)
        user.save()
        usuario = Usuario.objects.create(user=user, nome=nome, data_nascimento=data_nascimento)
        login(request, user)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('home')
    return render(request, 'cadastro.html')
 
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos')
            
    return render(request, 'login.html')

@login_required
def home(request):
    produtos = Produto.objects.all() 
    return render(request, "home.html", {"produtos": produtos})

@login_required
def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user.usuario)
    item_carrinho, created = ItensCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 0}
    )
    if produto.quantidade > item_carrinho.quantidade:
        item_carrinho.quantidade += 1
        item_carrinho.save()
        messages.success(request, f'"{produto.nome}" foi adicionado ao carrinho.')
    else:
        messages.error(request, f'Não há mais estoque disponível para "{produto.nome}".')
    
    return redirect('home')

@login_required
def carrinho_view(request):
    usuario_profile, created = Usuario.objects.get_or_create(user=request.user)
    if created:
        usuario_profile.nome = request.user.first_name or request.user.username
        usuario_profile.save()
    carrinho, _ = Carrinho.objects.get_or_create(usuario=usuario_profile)
    itens = carrinho.itenscarrinho_set.all()
    total_carrinho = carrinho.total()
    context = {
        'itens_carrinho': itens,
        'total_carrinho': total_carrinho,
    }
    return render(request, 'carrinho.html', context)

@login_required
def remover_do_carrinho(request, id):
    item_carrinho = get_object_or_404(ItensCarrinho, id=id)
    if item_carrinho.carrinho.usuario == request.user.usuario:
        nome_produto = item_carrinho.produto.nome
        item_carrinho.delete()
        messages.success(request, f'"{nome_produto}" foi removido do carrinho.')
    else:
        messages.error(request, "Você não tem permissão para remover este item.")
    return redirect('carrinho')

@login_required 
@has_permission_decorator('cadastrar_produto')
def cadastrar_produto_view(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('home')
    else:
        form = ProdutoForm()
    return render(request, 'cadastrar_produto.html', {'form': form})

@login_required
@has_permission_decorator('editar_produto')
def editar_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('home')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})

@login_required
@has_permission_decorator('remover_produto')
def remover_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto removido com sucesso!')
        return redirect('home')
    return render(request, 'remover_produto.html', {'produto': produto})

@login_required
def aumentar_quantidade(request, item_id): 
    item = get_object_or_404(ItensCarrinho, id=item_id)
    if item.carrinho.usuario == request.user.usuario:
        item.quantidade += 1
        item.save()
    return redirect('carrinho')

@login_required
def diminuir_quantidade(request, item_id):
    item = get_object_or_404(ItensCarrinho, id=item_id)
    if item.carrinho.usuario == request.user.usuario:
        if item.quantidade > 1:
            item.quantidade -= 1
            item.save()
        else:
            item.delete()
            messages.info(request, f'"{item.produto.nome}" foi removido do carrinho.')
    return redirect('carrinho')

@login_required
@transaction.atomic
def finalizar_pedido(request):
    carrinho_itens = ItensCarrinho.objects.filter(carrinho__usuario=request.user.usuario)
    if not carrinho_itens.exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')
    pedido = Pedido.objects.create(usuario=request.user, status='finalizado')
    total_pedido = 0
    for item_carrinho in carrinho_itens:
        produto = item_carrinho.produto
        
        if produto.quantidade < item_carrinho.quantidade:
            messages.error(request, f'Estoque insuficiente para {produto.nome}.')
            transaction.set_rollback(True) 
            return redirect('carrinho')
        produto.quantidade -= item_carrinho.quantidade
        produto.save()

        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=item_carrinho.quantidade,
            preco_unitario=produto.preco
        )
        total_pedido += item_carrinho.subtotal() 
    pedido.total = total_pedido
    pedido.save()
    carrinho_itens.delete()
    messages.success(request, 'Seu pedido foi finalizado com sucesso!')
    return redirect('perfil')

@login_required
def ver_perfil(request):
    
    print(f"--- Acessando a view ver_perfil para o usuário: {request.user.username} ---")

    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data_criacao').prefetch_related('itens__produto')
    
    context = {
        'pedidos': pedidos
    }
    
    return render(request, 'perfil.html', context)

@login_required
def limpar_carrinho(request):
    ItensCarrinho.objects.filter(carrinho__usuario=request.user.usuario).delete()
    messages.success(request, 'Seu carrinho foi esvaziado com sucesso!')
    return redirect('carrinho')
def is_superuser(user):
    
    return user.is_superuser

@user_passes_test(is_superuser, login_url='/login/')
def listar_usuarios(request):
    usuarios = User.objects.all().order_by('username')
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})



@user_passes_test(is_superuser, login_url='/login/')
def gerenciar_admin(request, user_id):

    GROUP_NAME = 'administradores'
    PERMISSOES_CODINOMES = ['cadastrar_produto', 'editar_produto', 'remover_produto']
    
    print(f"\n\n--- INICIANDO DIAGNÓSTICO DA VIEW HÍBRIDA 'gerenciar_admin' ---")
    
    if request.method == 'POST':
        print("Método da requisição é POST. Processando...")
        usuario_para_modificar = get_object_or_404(User, id=user_id)
        print(f"Usuário a ser modificado encontrado: '{usuario_para_modificar.username}'")

        if usuario_para_modificar.is_superuser:
            messages.error(request, 'Não é possível alterar o status de um Superusuário.')
            return redirect('listar_usuarios')

   
        try:
            print(f"Buscando o grupo '{GROUP_NAME}'...")
            admin_group = Group.objects.get(name=GROUP_NAME) 
            print(">> SUCESSO: Grupo encontrado.")
        except Group.DoesNotExist:
            print(f">> ERRO FATAL: O grupo '{GROUP_NAME}' NÃO EXISTE. Crie-o no painel /admin.")
            messages.error(request, f"O grupo de permissão '{GROUP_NAME}' não foi encontrado.")
            return redirect('listar_usuarios')

        try:
            print(f"Buscando as permissões individuais: {PERMISSOES_CODINOMES}...")
            permissoes = Permission.objects.filter(codename__in=PERMISSOES_CODINOMES)
            if permissoes.count() != len(PERMISSOES_CODINOMES):
                print(">> ERRO FATAL: Uma ou mais permissões individuais não foram encontradas.")
                messages.error(request, "Uma ou mais permissões necessárias não foram encontradas no banco de dados.")
                return redirect('listar_usuarios')
            print(">> SUCESSO: Todas as permissões individuais foram encontradas.")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao buscar as permissões: {e}")
            return redirect('listar_usuarios')

       
        if usuario_para_modificar.is_staff:
            print(f"'{usuario_para_modificar.username}' JÁ É staff. Removendo acesso...")
            usuario_para_modificar.groups.remove(admin_group)
            usuario_para_modificar.user_permissions.remove(*permissoes) 
            usuario_para_modificar.is_staff = False
            print(">> AÇÃO: Removido do grupo, permissões diretas removidas, is_staff=False.")
            messages.success(request, f'As permissões de Admin foram REMOVIDAS de {usuario_para_modificar.username}.')
        

        else:
            print(f"'{usuario_para_modificar.username}' NÃO É staff. Adicionando acesso...")
            usuario_para_modificar.groups.add(admin_group) # Adiciona ao grupo
            usuario_para_modificar.user_permissions.add(*permissoes) # Adiciona permissões diretas
            usuario_para_modificar.is_staff = True
            print(">> AÇÃO: Adicionado ao grupo, permissões diretas adicionadas, is_staff=True.")
            messages.success(request, f'{usuario_para_modificar.username} agora é um Admin!')
            
        print("Salvando alterações no banco de dados...")
        usuario_para_modificar.save()
        print(">> SUCESSO: Alterações salvas.")
        
        print("--- FIM DO DIAGNÓSTICO ---")
        return redirect('listar_usuarios')
    
    return redirect('listar_usuarios')

@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def admin_pedidos(request):
    todos_pedidos = Pedido.objects.all().order_by('-data_criacao').prefetch_related(
        'usuario__usuario',  
        'itens', 
        'itens__produto'
    )
    
    context = {
        'pedidos': todos_pedidos
    }
    
    return render(request, 'admin_pedidos.html', context)

@login_required
@transaction.atomic
def finalizar_pedido(request):
    carrinho_itens = ItensCarrinho.objects.filter(carrinho__usuario=request.user.usuario)
    if not carrinho_itens.exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')
    pedido = Pedido.objects.create(usuario=request.user, status='finalizado')
    total_pedido = 0
    for item_carrinho in carrinho_itens:
        produto = item_carrinho.produto
        if produto.quantidade < item_carrinho.quantidade:
            messages.error(request, f'Estoque insuficiente para {produto.nome}.')
            transaction.set_rollback(True)
            return redirect('carrinho')
        produto.quantidade -= item_carrinho.quantidade
        produto.save()
        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=item_carrinho.quantidade,
            preco_unitario=produto.preco
        )
        total_pedido += item_carrinho.subtotal() 
    
    pedido.total = total_pedido
    pedido.save()

    try:
        subject = f"Confirmação do Pedido #{pedido.id} - TT ANABOLIC"
        context = {
            'user': request.user,
            'pedido': pedido
        }
        html_message = render_to_string('confirmacao_pedido_email.html', context)
        
        send_mail(
            subject,
            'Seu pedido foi confirmado!', 
            settings.DEFAULT_FROM_EMAIL, 
            [request.user.email], 
            html_message=html_message, 
            fail_silently=False,
        )
    except Exception as e:
        print(f"ERRO ao enviar email de confirmação: {e}")


    carrinho_itens.delete()

    messages.success(request, 'Seu pedido foi finalizado com sucesso!')
    return redirect('perfil')

@login_required
def perfil_endereco(request):
    try:
        endereco_existente = Endereco.objects.get(usuario=request.user)
    except Endereco.DoesNotExist:
        endereco_existente = None

    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco_existente)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user 
            endereco.save()
            messages.success(request, 'Endereço salvo com sucesso!')
   
            return redirect('perfil') 
            
    else:
        form = EnderecoForm(instance=endereco_existente)

    context = {
        'form': form
    }

    return render(request, 'perfil_endereco.html', context)

@login_required
def checkout_endereco(request):
    try:
        endereco_existente = Endereco.objects.get(usuario=request.user)
    except Endereco.DoesNotExist:
        endereco_existente = None

    if not ItensCarrinho.objects.filter(carrinho__usuario=request.user.usuario).exists():
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('carrinho')

    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco_existente)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            return redirect('finalizar_pedido')
    else:
        form = EnderecoForm(instance=endereco_existente)

    context = {
        'form': form
    }
    return render(request, 'checkout_endereco.html', context)