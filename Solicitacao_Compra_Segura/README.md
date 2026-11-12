# Solicitação de Compra Segura — Etapa 1

## Cenário e objetivo
Um responsável solicita a compra de materiais. O setor de compras verifica a assinatura digital antes de receber a solicitação como autêntica. O texto inclui material, quantidade e justificativa. Alterar a quantidade depois da assinatura deve causar rejeição. A assinatura válida permite conferir origem e integridade. A aprovação financeira da compra é uma decisão posterior.

## Executar
Abra esta pasta no VS Code e rode:
```bash
python -m pip install -r requirements.txt
python interface.py
```
A interface usa Tkinter. No Windows ele normalmente acompanha Python. No Linux pode ser necessário o pacote python3-tk.

## Demonstrar
1. Digite a solicitação no campo Responsável. Exemplo: Material: papel A4 | Quantidade: 10 resmas | Justificativa: reposição do estoque.
2. Clique em Assinar e enviar e depois em Verificar solicitação. O setor de compras recebe o texto verificado.
3. Na solicitação recebida, altere 10 resmas para 100 resmas. Clique diretamente em Verificar solicitação. A solicitação é bloqueada.
4. Clique em Assinar e enviar para reiniciar. Clique em Testar outra chave. A assinatura de outra chave é rejeitada.
O campo é texto livre. Todos os caracteres do texto enviado são assinados.

## Código e decisões
- interface.py apresenta o responsável, a mensagem recebida e o setor de compras em uma janela. O envio ocorre em memória.
- responsavel.py gera e persiste o par Ed25519 e permite exportar solicitações assinadas em JSON.
- compras.py verifica os arquivos usando a chave pública previamente confiada.
- demonstracao.py reproduz os testes em uma pasta temporária. O resultado executado está em evidencias/testes.txt.
- cryptography implementa o algoritmo Ed25519. O texto é convertido para UTF-8. A assinatura bruta tem 64 bytes. Base64 permite representá-la no JSON.
- A chave privada é armazenada em PEM/PKCS#8 e a pública em PEM/SubjectPublicKeyInfo. A privada deve permanecer com o responsável. A pública é configurada no setor de compras por canal confiável.

## Testes no terminal
```bash
python demonstracao.py
python responsavel.py gerar-chaves
python responsavel.py enviar pedido.json
python compras.py pedido.json
```
Os testes abrangem solicitação original aceita, quantidade adulterada rejeitada, assinatura de outra chave rejeitada e JSON inválido bloqueado. O script temporário remove a chave privada antes da verificação para demonstrar que o destinatário precisa apenas da pública.

## Sigilo, autenticidade e confiança
A assinatura permite verificar integridade e autenticidade associada à chave confiada. O texto permanece legível. Cifragem atenderia à confidencialidade.
Um certificado digital associa identidade e chave pública, com assinatura de uma autoridade certificadora. A PKI organiza emissão, validação de cadeias e revogação. Este protótipo usa configuração direta da chave pública confiável. Aceitar uma chave enviada pelo próprio remetente sem validação permitiria aceitar identidades falsas.

## Gestão de chaves e limitações
As chaves são persistidas em chaves/ e ignoradas pelo Git. A chave privada local de laboratório fica sem senha. O programa solicita permissões restritas no sistema de arquivos, cujo efeito depende do sistema operacional. Em produção, a guarda deve ser feita com proteção adequada e procedimento de rotação.
O protótipo não controla reenvio de solicitações antigas nem autenticação de usuários. Para controlar reenvios, seria necessário assinar identificador e validade e registrar as solicitações já processadas. Cadastro/login pertencem à próxima etapa.
A interface simula os dois setores no mesmo computador. Para exportação e verificação por arquivos, use os comandos acima. Use dados fictícios.



## Referências
- Atividade Avaliativa — Projeto Integrador | Segurança Aplicada ao Desenvolvimento.
- Aula 01 — Unidade 02, Segurança aplicada ao desenvolvimento.
- https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ed25519/
- https://www.rfc-editor.org/rfc/rfc8032
