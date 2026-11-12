"""Verifica um aviso usando a chave pública configurada localmente."""

import argparse
import base64
import binascii
import json
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pacote", type=Path)
    parser.add_argument(
        "--chave-publica",
        type=Path,
        default=Path(__file__).resolve().parent / "chaves" / "responsavel_publica.pem",
        help="Chave previamente confiada pelo operador do mural.",
    )
    args = parser.parse_args()

    try:
        chave = serialization.load_pem_public_key(args.chave_publica.read_bytes())
        if not isinstance(chave, Ed25519PublicKey):
            raise ValueError("A chave pública precisa ser Ed25519.")
        pacote = json.loads(args.pacote.read_text(encoding="utf-8"))
        if not isinstance(pacote, dict):
            raise ValueError("O pacote precisa ser um objeto JSON.")

        mensagem = pacote.get("mensagem")
        assinatura = pacote.get("assinatura")
        if not isinstance(mensagem, str) or not mensagem.strip() or not isinstance(assinatura, str):
            raise ValueError("O pacote precisa conter mensagem e assinatura em texto.")
        assinatura_bytes = base64.b64decode(assinatura, validate=True)
        if len(assinatura_bytes) != 64:
            raise ValueError("A assinatura Ed25519 deve ter 64 bytes.")
        chave.verify(assinatura_bytes, mensagem.encode("utf-8"))
    except InvalidSignature:
        parser.exit(1, "REJEITADO: assinatura inválida. Solicitação bloqueada.\n")
    except (OSError, ValueError, binascii.Error) as erro:
        parser.exit(2, f"ERRO: solicitação bloqueada. {erro}\n")

    print("ACEITO: assinatura válida.")
    print(f"Solicitação verificada: {mensagem}")


if __name__ == "__main__":
    main()
