# Etapa 2 — Hash e autenticação segura
UNIT Campus Farolândia — ADS
Emmanuel Carlos Silva, Célio Abdias e Marcos Matheus.
Docente Ana Carla do Nascimento Santos.

## Objetivo
Cadastrar responsáveis e permitir acesso à interface de solicitações de compra após login. A primeira etapa continua disponível após autenticação.

## Executar
Abra a pasta Etapa_2 no VS Code.
python -m pip install -r requirements.txt
python interface.py

Na primeira utilização, escolha um usuário e uma senha de 15 a 128 caracteres e clique em Cadastrar. Digite novamente a senha e clique em Entrar. O campo de senha é limpo após cada tentativa. Sair da conta retorna à tela de login. Os usuários ficam persistidos em dados/usuarios.db, criado automaticamente.

## Implementação
Python e Tkinter apresentam cadastro, login e solicitações. SQLite armazena usuário e senha_hash. As consultas usam parâmetros. O nome de usuário é normalizado e tem restrição de unicidade no banco. A senha é usada exatamente como digitada.
argon2-cffi 25.1.0 gera Argon2id com memória de 65536 KiB (64 MiB), três iterações, paralelismo quatro, salt aleatório de 16 bytes e hash de 32 bytes. A string armazenada contém algoritmo, versão, parâmetros, salt e hash. Portanto, o salt já fica persistido junto ao hash.
PasswordHasher.verify faz a comparação por meio da biblioteca. A aplicação não compara hashes manualmente. Após um login válido, check_needs_rehash permite atualizar parâmetros antigos.
Hash é uma derivação de sentido único. A senha original não precisa ser recuperada. SHA-256 isolado é rápido e facilita testar muitas tentativas de senha. Argon2id exige tempo e memória e utiliza salt aleatório por registro. Salt diferencia resultados de senhas iguais e reduz o aproveitamento de tabelas pré-calculadas.

## Testes
python testar_etapa_2.py
python demonstracao.py

Os resultados executados estão em evidencias/etapa_2.txt e evidencias/etapa_1_regressao.txt. Os testes criam usuários fictícios em pasta temporária.
Para demonstrar na interface, cadastre uma conta, tente entrar com senha errada, entre com a correta, envie uma solicitação, saia e entre novamente. Feche e reabra o programa para demonstrar persistência.
O registro protegido de exemplo nas evidências mostra os parâmetros e o salt dentro da string Argon2id.

## Limites
O login restringe o fluxo da interface desktop. Quem controla os arquivos e o Python local pode executar diretamente os scripts da etapa 1. O protótipo não constitui uma fronteira de autorização contra o administrador do computador.
O cadastro é aberto para laboratório. Os usuários compartilham a chave de assinatura institucional da primeira etapa. Não há assinatura individual por conta, bloqueio por tentativas nem recuperação de senha. O banco não é criptografado e precisa de proteção por permissões e backups. O diretório dados é ignorado no Git.
A interface ainda precisa de validação visual no computador da equipe. Os testes automatizados exercitam autenticação e assinatura pelos módulos reais.
Melhorias futuras incluem autorização por perfil, cadastro administrativo, limitação de tentativas e separação de serviço e interface.

## Apresentação
Emmanuel apresenta cenário, cadastro e login.
Célio explica hash, salt, Argon2id e por que SHA-256 isolado não atende a senhas.
Marcos demonstra senha incorreta, login correto, persistência e resultados dos testes.
Essa divisão é uma sugestão para estudo do grupo.

## Referências
SANTOS, Ana Carla do Nascimento. Atividade avaliativa — Projeto Integrador: Segurança Aplicada ao Desenvolvimento. UNIT, 2026.
SANTOS, Ana Carla do Nascimento. Aula 01 — Unidade 02. UNIT, 2026.
ARGON2-CFFI. How to Hash a Password. Disponível em https://argon2-cffi.readthedocs.io/en/stable/howto.html. Acesso em 18 nov. 2026.
Repositório informado pelo grupo: https://github.com/emmanuelcarlos888-glitch/trabalho-seguran-a.git
Esta versão foi preparada a partir do pacote entregue anteriormente. Não foi publicada automaticamente no GitHub.
