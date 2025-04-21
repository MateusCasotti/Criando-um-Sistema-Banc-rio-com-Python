class Livro:
    def __init__(self, titulo, autor, ano_publicacao):
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.disponivel = True

    def emprestar(self):
        if self.disponivel:
            self.disponivel = False
            print(f"Livro '{self.titulo}' emprestado com sucesso.")
        else:
            print(f"Livro '{self.titulo}' já está emprestado.")

    def devolver(self):
        if not self.disponivel:
            self.disponivel = True
            print(f"Livro '{self.titulo}' devolvido com sucesso.")
        else:
            print(f"Livro '{self.titulo}' já estava disponível.")


class Biblioteca:
    def __init__(self):
        self.acervo = []

    def adicionar_livro(self, livro):
        self.acervo.append(livro)
        print(f"Livro '{livro.titulo}' adicionado à biblioteca.")

    def listar_livros(self):
        print("\n=== Acervo da Biblioteca ===")
        for livro in self.acervo:
            status = "Disponível" if livro.disponivel else "Emprestado"
            print(f"{livro.titulo} - {livro.autor} ({livro.ano_publicacao}) - {status}")
        print("============================\n")

    def emprestar_livro(self, titulo):
        for livro in self.acervo:
            if livro.titulo.lower() == titulo.lower():
                livro.emprestar()
                return
        print(f"Livro '{titulo}' não encontrado no acervo.")

    def devolver_livro(self, titulo):
        for livro in self.acervo:
            if livro.titulo.lower() == titulo.lower():
                livro.devolver()
                return
        print(f"Livro '{titulo}' não encontrado no acervo.")


# Exemplo de uso:
if __name__ == "__main__":
    biblioteca = Biblioteca()

    livro1 = Livro("1984", "George Orwell", 1949)
    livro2 = Livro("Dom Casmurro", "Machado de Assis", 1899)

    biblioteca.adicionar_livro(livro1)
    biblioteca.adicionar_livro(livro2)

    biblioteca.listar_livros()
    biblioteca.emprestar_livro("1984")
    biblioteca.listar_livros()
    biblioteca.devolver_livro("1984")
    biblioteca.listar_livros()
