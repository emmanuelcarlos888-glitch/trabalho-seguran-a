from tempfile import TemporaryDirectory
from pathlib import Path
import autenticacao as a

with TemporaryDirectory() as pasta:
    a.BANCO = Path(pasta) / "usuarios.db"
    senha = "Minha frase de teste 2026!"
    a.cadastrar("alice", senha)
    a.cadastrar("bruno", senha)
    assert a.autenticar("alice", senha)
    print("PASSOU — login correto.")
    assert not a.autenticar("alice", "senha incorreta")
    print("PASSOU — senha incorreta rejeitada.")
    assert not a.autenticar("inexistente", senha)
    print("PASSOU — usuário inexistente rejeitado.")
    try:
        a.cadastrar("ALICE", senha)
    except ValueError:
        print("PASSOU — cadastro duplicado rejeitado.")
    else:
        raise AssertionError("Duplicidade aceita")
    with a.conectar() as c:
        hashes = [r[0] for r in c.execute("SELECT senha_hash FROM usuarios ORDER BY usuario")]
    assert hashes[0] != hashes[1]
    assert all(h.startswith("$argon2id$") and senha not in h for h in hashes)
    print("PASSOU — mesma senha tem salts e hashes diferentes.")
    print("Registro fictício protegido:", hashes[0])
    assert a.autenticar("alice", senha)
    print("PASSOU — cadastro persistiu entre conexões.")
    try:
        a.cadastrar("curta", "123")
    except ValueError:
        print("PASSOU — senha curta rejeitada.")
    else:
        raise AssertionError("Senha curta aceita")
print("Todos os testes da etapa 2 passaram.")
