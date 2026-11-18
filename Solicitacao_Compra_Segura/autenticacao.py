"""Cadastro persistente e verificação de senhas com Argon2id."""
import sqlite3
from pathlib import Path
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerificationError, InvalidHashError

BANCO = Path(__file__).resolve().parent / "dados" / "usuarios.db"
HASHER = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4,
                        hash_len=32, salt_len=16, type=Type.ID)


def conectar():
    BANCO.parent.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(BANCO)
    conexao.execute("CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT PRIMARY KEY, senha_hash TEXT NOT NULL)")
    return conexao


def cadastrar(usuario, senha):
    usuario = usuario.strip().casefold()
    if not 3 <= len(usuario) <= 80:
        raise ValueError("O usuário deve ter entre 3 e 80 caracteres.")
    if not 15 <= len(senha) <= 128:
        raise ValueError("A senha deve ter entre 15 e 128 caracteres.")
    protegido = HASHER.hash(senha)
    try:
        with conectar() as conexao:
            conexao.execute("INSERT INTO usuarios VALUES (?, ?)", (usuario, protegido))
    except sqlite3.IntegrityError:
        raise ValueError("Este usuário já está cadastrado.") from None
    return usuario


def autenticar(usuario, senha):
    usuario = usuario.strip().casefold()
    with conectar() as conexao:
        linha = conexao.execute("SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        if linha is None or len(senha) > 128:
            return False
        try:
            HASHER.verify(linha[0], senha)
        except (VerificationError, InvalidHashError):
            return False
        if HASHER.check_needs_rehash(linha[0]):
            conexao.execute("UPDATE usuarios SET senha_hash = ? WHERE usuario = ?",
                           (HASHER.hash(senha), usuario))
    return True
