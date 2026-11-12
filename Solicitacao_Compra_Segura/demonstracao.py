"""Reproduz os testes em um laboratório temporário com chaves fictícias."""

import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

AVISO = "Material: papel A4 | Quantidade: 10 resmas | Justificativa: reposição do estoque."


def executar(pasta, argumentos, esperado, entrada=None):
    print(f"> python {' '.join(argumentos)}", flush=True)
    resultado = subprocess.run(
        [sys.executable, *argumentos], cwd=pasta, input=entrada,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    print(resultado.stdout, end="")
    print(f"Código de saída: {resultado.returncode} (esperado: {esperado})\n")
    if resultado.returncode != esperado:
        raise SystemExit("O teste retornou um código diferente do esperado.")


with TemporaryDirectory() as temporaria:
    pasta = Path(temporaria)
    for nome in ("responsavel.py", "compras.py"):
        shutil.copy2(Path(__file__).resolve().parent / nome, pasta / nome)

    executar(pasta, ["responsavel.py", "gerar-chaves"], 0)
    executar(pasta, ["responsavel.py", "enviar", "aviso.json"], 0, AVISO + "\n")
    # A partir daqui, a verificação ocorre sem a chave privada.
    (pasta / "chaves" / "responsavel_privada.pem").unlink()

    print("TESTE 1 — aviso original")
    executar(pasta, ["compras.py", "aviso.json"], 0)

    original = json.loads((pasta / "aviso.json").read_text(encoding="utf-8"))
    adulterado = dict(original, mensagem=AVISO.replace("10 resmas", "100 resmas"))
    (pasta / "aviso_adulterado.json").write_text(json.dumps(adulterado), encoding="utf-8")
    print("TESTE 2 — conteúdo alterado, assinatura preservada")
    executar(pasta, ["compras.py", "aviso_adulterado.json"], 1)

    outra_assinatura = Ed25519PrivateKey.generate().sign(AVISO.encode("utf-8"))
    forjado = dict(original, assinatura=base64.b64encode(outra_assinatura).decode("ascii"))
    (pasta / "aviso_forjado.json").write_text(json.dumps(forjado), encoding="utf-8")
    print("TESTE 3 — conteúdo preservado, assinatura feita por outra chave")
    executar(pasta, ["compras.py", "aviso_forjado.json"], 1)

    (pasta / "aviso_invalido.json").write_text("{", encoding="utf-8")
    print("TESTE 4 — pacote JSON incompleto")
    executar(pasta, ["compras.py", "aviso_invalido.json"], 2)

print("Todos os testes passaram.")
