from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from rolepermissions.roles import AbstractUserRole
class Usuario(models.Model):
    nome = models.CharField('nome', max_length=100,null=False)
    data_nascimento = models.DateField('data_nascimento',null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome    
    
class Produto (models.Model):
    nome = models.CharField('nome', max_length=100,null=False)
    descricao = models.CharField('descricao', max_length=1000,null=False)
    preco = models.DecimalField('preco', max_digits=10, decimal_places=2)
    quantidade = models.IntegerField('quantidade',null=False)
    imagem = models.ImageField(upload_to='Produto/', blank=True, null=True)
    class Meta:
        permissions = [
            ("cadastrar_produto", "Pode cadastrar produtos"),
            ("editar_produto", "Pode editar produtos"),
            ("remover_produto", "Pode remover produtos"),
        ]
    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"Carrinho de {self.usuario.nome}"
    def total(self):
        return sum([item.subtotal() for item in self.itenscarrinho_set.all()]) #funçao para calcular o total do carrinho (sum) obs

class ItensCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0) # Adicionado um valor padrao
    def subtotal(self):
        return self.produto.preco * self.quantidade
    def __str__(self):
        return self.produto.nome

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} no Pedido #{self.pedido.id}"
    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
class Administrador(AbstractUserRole):
    role_name = 'administradores' 
    available_permissions = {
        'cadastrar_produto': True,
        'editar_produto': True,
        'remover_produto': True,
    }

class UsuarioComum(AbstractUserRole):
    role_name = 'usuario_comum'
    available_permissions = {} 
    
class Endereco(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    def __str__(self):
        return f"Endereço de {self.usuario.username}"