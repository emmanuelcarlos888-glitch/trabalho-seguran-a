"""Interface desktop para a demonstração da primeira entrega."""
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from responsavel import preparar_chaves, PRIVADA, PUBLICA


def abrir_solicitacoes(janela, usuario):
    janela.title("Solicitação de Compra Segura • Etapa 2")
    janela.geometry("950x720")
    janela.minsize(760, 640)
    janela.configure(bg="#eef2f7")
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TFrame", background="#eef2f7")
    estilo.configure("TLabel", background="#eef2f7", font=("Segoe UI", 11))
    estilo.configure("TButton", font=("Segoe UI", 11), padding=10)
    estilo.configure("Titulo.TLabel", font=("Segoe UI", 24, "bold"), foreground="#132544")
    estilo.configure("Secao.TLabel", font=("Segoe UI", 13, "bold"))
    painel = ttk.Frame(janela, padding=24)
    painel.pack(fill="both", expand=True)
    ttk.Label(painel, text=f"Usuário conectado: {usuario}").pack(anchor="w")
    ttk.Button(painel, text="Sair da conta", command=lambda: voltar_login(janela)).pack(anchor="e")
    ttk.Label(painel, text="Solicitação de Compra Segura", style="Titulo.TLabel").pack(anchor="w")
    ttk.Label(painel, text="Assinatura digital • Ed25519 • Laboratório local").pack(anchor="w", pady=(0, 20))
    estado = {"assinatura": None, "publica": None}
    ttk.Label(painel, text="1. Responsável — escreva sua solicitação", style="Secao.TLabel").pack(anchor="w")
    origem = tk.Text(painel, height=4, font=("Segoe UI", 12), wrap="word", relief="flat", padx=12, pady=10)
    origem.pack(fill="x", pady=8)
    origem.insert("1.0", "Material: papel A4 | Quantidade: 10 resmas | Justificativa: reposição do estoque.")
    ttk.Label(painel, text="2. Solicitação recebida — edite aqui para simular adulteração", style="Secao.TLabel").pack(anchor="w", pady=(12, 0))
    recebido = tk.Text(painel, height=4, font=("Segoe UI", 12), wrap="word", relief="flat", padx=12, pady=10)
    recebido.pack(fill="x", pady=8)
    status = tk.StringVar(value="Digite a solicitação e clique em Assinar e enviar.")
    mural = tk.Text(painel, height=5, font=("Segoe UI", 12), wrap="word", relief="flat", padx=12, pady=10, state="disabled")

    def mostrar(texto):
        mural.configure(state="normal")
        mural.delete("1.0", "end")
        mural.insert("1.0", texto)
        mural.configure(state="disabled")

    def enviar():
        mensagem = origem.get("1.0", "end-1c")
        if not mensagem.strip():
            messagebox.showwarning("Solicitação vazia", "Digite uma solicitação antes de enviar.")
            return
        try:
            preparar_chaves()
            privada = serialization.load_pem_private_key(PRIVADA.read_bytes(), password=None)
            publica = serialization.load_pem_public_key(PUBLICA.read_bytes())
            assinatura = privada.sign(mensagem.encode("utf-8"))
        except (OSError, ValueError) as erro:
            messagebox.showerror("Falha ao assinar", str(erro))
            return
        estado.update(assinatura=assinatura, publica=publica)
        recebido.delete("1.0", "end")
        recebido.insert("1.0", mensagem)
        mostrar("")
        status.set("Assinado pela responsável. Verifique o original ou altere a solicitação recebida.")

    def verificar():
        if estado["assinatura"] is None:
            messagebox.showinfo("Envio necessário", "Primeiro clique em Assinar e enviar.")
            return
        mensagem = recebido.get("1.0", "end-1c")
        try:
            estado["publica"].verify(estado["assinatura"], mensagem.encode("utf-8"))
        except InvalidSignature:
            status.set("REJEITADO — assinatura inválida. Solicitação bloqueada.")
            mostrar("")
            return
        status.set("ACEITO — assinatura válida. Solicitação recebida pelo setor de compras.")
        mostrar(mensagem)

    def outra_chave():
        if estado["assinatura"] is None:
            messagebox.showinfo("Envio necessário", "Primeiro clique em Assinar e enviar.")
            return
        mensagem = recebido.get("1.0", "end-1c")
        estado["assinatura"] = Ed25519PrivateKey.generate().sign(mensagem.encode("utf-8"))
        verificar()

    botoes = ttk.Frame(painel)
    botoes.pack(fill="x", pady=8)
    ttk.Button(botoes, text="Assinar e enviar", command=enviar).pack(side="left", padx=(0, 8))
    ttk.Button(botoes, text="Verificar solicitação", command=verificar).pack(side="left", padx=(0, 8))
    ttk.Button(botoes, text="Testar outra chave", command=outra_chave).pack(side="left")
    ttk.Label(painel, textvariable=status, wraplength=840).pack(anchor="w", pady=12)
    ttk.Label(painel, text="3. Setor de compras — solicitação verificada", style="Secao.TLabel").pack(anchor="w")
    mural.pack(fill="both", expand=True, pady=8)
    ttk.Label(painel, text="Para reiniciar um teste, clique em Assinar e enviar. As chaves ficam na pasta chaves.", wraplength=840).pack(anchor="w")




def voltar_login(janela):
    for widget in janela.winfo_children():
        widget.destroy()
    mostrar_login(janela)


def mostrar_login(janela):
    from autenticacao import cadastrar, autenticar
    import sqlite3
    janela.title("Solicitação de Compra Segura • Acesso")
    janela.geometry("950x780")
    painel = ttk.Frame(janela, padding=40)
    painel.pack(expand=True)
    ttk.Label(painel, text="Solicitação de Compra Segura", font=("Segoe UI", 22, "bold")).pack(pady=12)
    ttk.Label(painel, text="Cadastre sua conta ou entre para acessar as solicitações.").pack(pady=8)
    ttk.Label(painel, text="Usuário").pack(anchor="w")
    usuario = ttk.Entry(painel, width=45)
    usuario.pack(pady=8)
    ttk.Label(painel, text="Senha • 6 a 128 caracteres no cadastro").pack(anchor="w")
    senha = ttk.Entry(painel, width=45, show="*")
    senha.pack(pady=8)
    retorno = tk.StringVar()
    ttk.Label(painel, textvariable=retorno, wraplength=550).pack(pady=10)

    def executar(cadastro=False):
        nome, segredo = usuario.get(), senha.get()
        try:
            if cadastro:
                cadastrar(nome, segredo)
                retorno.set("Conta cadastrada. Digite a senha e clique em Entrar.")
            elif autenticar(nome, segredo):
                for widget in janela.winfo_children():
                    widget.destroy()
                abrir_solicitacoes(janela, nome.strip().casefold())
                return
            else:
                retorno.set("Usuário ou senha inválidos.")
        except ValueError as erro:
            retorno.set(str(erro))
        except (sqlite3.Error, OSError):
            retorno.set("Não foi possível acessar o cadastro local.")
        finally:
            if senha.winfo_exists():
                senha.delete(0, "end")

    ttk.Button(painel, text="Entrar", command=executar).pack(fill="x", pady=5)
    ttk.Button(painel, text="Cadastrar", command=lambda: executar(True)).pack(fill="x", pady=5)
    usuario.focus_set()


def iniciar():
    janela = tk.Tk()
    mostrar_login(janela)
    janela.mainloop()


if __name__ == "__main__":
    iniciar()
