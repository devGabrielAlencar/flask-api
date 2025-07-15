import flet as ft
import requests

# Lista global para armazenar clientes
clientes = []


def view_clientes(page: ft.Page):
    page.title = "CRM Clientes"

    formulario_container = ft.Column()
    lista_clientes_container = ft.Column()

    # Função para atualizar a lista de clientes na tela

    def listar_clientes(e=None):
        lista_clientes_container.controls.clear()

        try:
            response = requests.get("http://localhost:5000/clientes")
            if response.status_code == 200:
                dados = response.json()
                clientes.clear()
                clientes.extend(dados)

            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("❌ Erro ao buscar clientes da API"))
                page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Falha na conexão: {ex}"))
            page.snack_bar.open = True

        for index, cliente in enumerate(clientes):
            lista_clientes_container.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                f"{cliente['nome']} - {cliente['telefone']}", color=ft.Colors.BLACK),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, idx=index: editar_cliente(
                                    idx)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Excluir",
                                on_click=lambda e, idx=index: excluir_cliente(
                                    idx)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=5,
                    margin=ft.margin.only(bottom=5),
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    border_radius=5,
                )
            )
        page.update()
    # Função para excluir cliente

    def excluir_cliente(index):
        clientes.pop(index)
        listar_clientes(None)
        page.update()

    # Função para editar cliente
    def editar_cliente(index):
        cliente = clientes[index]
        formulario_container.controls.clear()

        nome = ft.TextField(label="Nome Completo",
                            value=cliente["nome"], width=400)
        endereco = ft.TextField(
            label="Endereço", value=cliente["endereco"], width=400)
        bairro = ft.TextField(
            label="Bairro", value=cliente["bairro"], width=400)
        telefone = ft.TextField(
            label="Telefone / WhatsApp", value=cliente["telefone"], width=400)
        tipo_suco = ft.Dropdown(
            label="Tipo de suco preferido",
            width=400,
            value=cliente["suco"],
            options=[
                ft.dropdown.Option("Laranja"),
                ft.dropdown.Option("Uva"),
                ft.dropdown.Option("Detox"),
                ft.dropdown.Option("Caju"),
                ft.dropdown.Option("Outro"),
            ],
        )
        observacoes = ft.TextField(
            label="Observações",
            value=cliente["obs"],
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=400,
        )

        def salvar_edicao(e):
            clientes[index] = {
                "nome": nome.value,
                "endereco": endereco.value,
                "bairro": bairro.value,
                "telefone": telefone.value,
                "suco": tipo_suco.value,
                "obs": observacoes.value,
            }
            formulario_container.controls.clear()
            listar_clientes()
            page.update()

        formulario_container.controls.append(
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        nome,
                        endereco,
                        bairro,
                        telefone,
                        tipo_suco,
                        observacoes,
                        ft.ElevatedButton("💾 Salvar edição",
                                          on_click=salvar_edicao, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        )
        page.update()

    # Função para adicionar novo cliente
    def add_clientes(e):
        # Se o formulário já estiver visível, fecha-o (limpa e esconde)
        if formulario_container.controls:
            formulario_container.controls.clear()
            page.update()
            return

        # Se não estiver aberto, cria o formulário normalmente
        nome = ft.TextField(label="Nome Completo", width=400)
        endereco = ft.TextField(label="Endereço", width=400)
        bairro = ft.TextField(label="Bairro", width=400)
        telefone = ft.TextField(label="Telefone / WhatsApp", width=400)
        tipo_suco = ft.Dropdown(
            label="Tipo de suco preferido",
            width=400,
            options=[
                ft.dropdown.Option("Laranja"),
                ft.dropdown.Option("Uva"),
                ft.dropdown.Option("Detox"),
                ft.dropdown.Option("Caju"),
                ft.dropdown.Option("Outro"),
            ],
        )

        def salvar_novo_cliente(e):

            cliente = {
                "nome": nome.value,
                "endereco": endereco.value,
                "bairro": bairro.value,
                "telefone": telefone.value,
                "suco": tipo_suco.value,
                "obs": ""
            }

            try:
                response = requests.post(
                    "http://localhost:5000/clientes", json=cliente)

                if response.status_code == 201:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("✅ Cliente salvo com sucesso!"))
                    clientes.append(cliente)  # opcional: atualiza local
                    listar_clientes()
                    page.update()
                else:
                    erro = response.json().get("erro", "Erro desconhecido")
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {erro}"))
                    page.update()

            except Exception as ex:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"❌ Erro ao conectar: {ex}"))

            formulario_container.controls.clear()
            page.snack_bar.open = True
            page.update()

        formulario_container.controls.append(
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    padding=20,
                    bgcolor=ft.Colors.ORANGE,
                    border_radius=10,
                    content=ft.Column(
                        [
                            nome,
                            endereco,
                            bairro,
                            telefone,
                            tipo_suco,
                            ft.ElevatedButton(
                                "💾 Salvar", on_click=salvar_novo_cliente, width=200),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )
        )
        page.update()

    # Inicializa a lista
    view = ft.View(
        route="/clientes",
        controls=[
            ft.AppBar(title=ft.Text("👤 Clientes"), center_title=True),
            ft.Row(
                controls=[
                    ft.ElevatedButton("Adicionar clientes",
                                      on_click=add_clientes, width=200),
                    ft.ElevatedButton("Gerenciar clientes",
                                      on_click=listar_clientes, width=200),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),
            formulario_container,
            ft.Text("📋 Lista de Clientes:", size=16),
            lista_clientes_container,
        ]
    )

    return view
