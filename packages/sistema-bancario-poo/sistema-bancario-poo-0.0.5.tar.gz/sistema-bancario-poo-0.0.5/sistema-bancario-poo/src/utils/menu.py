class Menu:
    menu_1 = {
        "[d]": "Depositar",
        "[s]": "Sacar",
        "[e]": "Extrato",
        "[nc]": "Nova Conta",
        "[lc]": "Listar Contas",
        "[nu]": "Novo Usuário",
        "[q]": "Sair"
    }

    @classmethod
    def exibir_menu(cls):
        for key, value in cls.menu_1.items():
            print(f"{key}: {value}")


if __name__ == '__main__':
    Menu.exibir_menu()
