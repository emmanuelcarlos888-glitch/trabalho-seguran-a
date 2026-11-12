"""Gera as chaves locais e assina um aviso digitado pela responsável."""

import argparse
import base64
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

CHAVES = Path(__file__).resolve().parent / "chaves"
PRIVADA = CHAVES / "responsavel_privada.pem"
PUBLICA = CHAVES / "responsavel_publica.pem"


def preparar_chaves():
    CHAVES.mkdir(mode=0o700, exist_ok=True)
    if not PRIVADA.exists():
        chave = Ed25519PrivateKey.generate()
        dados = chave.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        with os.fdopen(os.open(PRIVADA, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as arquivo:
            arquivo.write(dados)

    chave = serialization.load_pem_private_key(PRIVADA.read_bytes(), password=None)
    if not isinstance(chave, Ed25519PrivateKey):
        raise ValueError("A chave privada precisa ser Ed25519.")
    dados_publicos = chave.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    if not PUBLICA.exists():
        with PUBLICA.open("xb") as arquivo:
            arquivo.write(dados_publicos)
    elif PUBLICA.read_bytes() != dados_publicos:
        raise ValueError("A chave pública existente não corresponde à privada.")
    print(f"Chaves prontas. Configure o mural com {PUBLICA.name} por um canal confiável.")


def assinar(destino):
    chave = serialization.load_pem_private_key(PRIVADA.read_bytes(), password=None)
    if not isinstance(chave, Ed25519PrivateKey):
        raise ValueError("A chave privada precisa ser Ed25519.")

    mensagem = input("Responsável — digite a solicitação: ")
    if not mensagem.strip():
        raise ValueError("A solicitação está vazia.")

    assinatura = chave.sign(mensagem.encode("utf-8"))
    pacote = {
        "mensagem": mensagem,
        "assinatura": base64.b64encode(assinatura).decode("ascii"),
    }
    with destino.open("x", encoding="utf-8") as arquivo:
        json.dump(pacote, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    print(f"Solicitação assinada e exportado para {destino}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest="comando", required=True)
    comandos.add_parser("gerar-chaves")
    envio = comandos.add_parser("enviar")
    envio.add_argument("destino", type=Path)
    args = parser.parse_args()

    try:
        if args.comando == "gerar-chaves":
            preparar_chaves()
        else:
            assinar(args.destino)
    except FileNotFoundError:
        parser.exit(2, "Arquivo ou pasta ausente. Gere as chaves e confira o caminho de saída.\n")
    except FileExistsError:
        parser.exit(2, "Arquivo já existente. Escolha outro nome ou repita após a geração das chaves.\n")
    except (OSError, ValueError, EOFError) as erro:
        parser.exit(2, f"Erro ao preparar o envio: {erro}\n")


if __name__ == "__main__":
    main()
