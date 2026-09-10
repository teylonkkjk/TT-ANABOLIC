# 🛒 TT Anabolic - E-commerce em Django

Um sistema completo de e-commerce desenvolvido em Python com o framework Django. O projeto abrange desde o cadastro de clientes e catálogo de produtos até o gerenciamento de permissões administrativas, controle de estoque e envio de e-mails de confirmação de pedidos.

## ✨ Funcionalidades

### 👤 Para os Clientes:
* **Autenticação:** Cadastro, Login e Logout seguros.
* **Catálogo e Carrinho:** Visualização de produtos, adição/remoção de itens no carrinho e controle dinâmico de quantidades.
* **Checkout e Endereços:** Cadastro de endereço de entrega integrado ao fluxo de finalização de compra.
* **Meus Pedidos:** Painel de perfil para acompanhar o histórico de compras.
* **Notificações:** Envio automático de e-mail em HTML confirmando a finalização do pedido.

### 🛡️ Para os Administradores (Controle de Permissões):
* **CRUD de Produtos:** Acesso restrito para cadastrar, editar e remover produtos.
* **Gestão de Estoque:** O sistema impede compras acima da quantidade disponível e debita do estoque automaticamente na venda.
* **Gestão de Usuários:** Superusuários podem promover ou rebaixar clientes ao cargo de "Administrador", utilizando a biblioteca `django-rolepermissions`.
* **Painel de Pedidos:** Tela exclusiva para visualização de todos os pedidos realizados na plataforma.

---

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3 & Django
* **Banco de Dados:** SQLite (padrão do Django, pode ser alterado para PostgreSQL)
* **Controle de Acesso:** `django-rolepermissions`
* **Frontend:** Templates HTML com estilização CSS / Bootstrap (adequar conforme seu front)
* **Envio de E-mails:** SMTP do Django (`django.core.mail`)

---

## ⚙️ Como rodar o projeto na sua máquina

### Pré-requisitos
Certifique-se de ter o **Python** e o **Git** instalados na sua máquina.

### Passo a passo

1. **Clone este repositório:**
   ```bash
   git clone [https://github.com/SEU-USUARIO/TT-ANABOLIC.git](https://github.com/SEU-USUARIO/TT-ANABOLIC.git)
   cd TT-ANABOLIC
