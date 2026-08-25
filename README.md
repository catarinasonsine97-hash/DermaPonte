# DermaPonte

MVP educacional de uma plataforma de triagem dermatológica e conexão entre pacientes e especialistas. O sistema recebe uma imagem e um questionário, aplica regras transparentes de priorização e apresenta profissionais disponíveis.

> O protótipo não realiza diagnóstico médico e não deve ser usado para decisão clínica real.

## Recursos do MVP

- captura de caso com imagem e sinais informados;
- classificação explicável de prioridade;
- fila clínica ordenada;
- busca de dermatologistas por UF;
- agendamento demonstrativo;
- confirmação, troca e cancelamento do agendamento;
- painel administrativo do Django.
- autenticação com perfis de paciente e profissional;
- área pessoal com histórico de casos;
- revisão profissional com justificativa e trilha de auditoria.

## Como funciona

1. O paciente envia uma imagem e responde ao questionário.
2. Regras explícitas combinam os sinais informados e calculam uma categoria de prioridade.
3. O caso entra na fila clínica, ordenada por prioridade e data de envio.
4. O paciente visualiza profissionais fictícios e realiza um agendamento demonstrativo.

As regras ficam isoladas em `triage/services.py`, permitindo auditoria e evolução sem misturar a lógica de priorização às páginas da aplicação.

## Tecnologias

- Python 3.12 e Django 5.2;
- SQLite;
- HTML e CSS responsivo;
- Pillow para validação de imagens;
- testes automatizados com Django TestCase.

## Segurança e limites

- não há diagnóstico por inteligência artificial nesta versão;
- a classificação é demonstrativa e não foi validada clinicamente;
- imagens de teste, banco local e segredos estão excluídos do repositório;
- qualquer uso real exigirá revisão clínica, segurança reforçada, adequação à LGPD e avaliação regulatória.

## Executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`.

### Contas locais de demonstração

Após executar `python manage.py seed_demo`:

- paciente: `demo-paciente` / `DermaPonte123!`;
- profissional: `demo-medico` / `DermaPonte123!`.

Essas credenciais existem apenas para desenvolvimento local e não devem ser usadas em produção.

## Próximas etapas

- agenda com horários reais e controle de concorrência;
- notificações e geolocalização;
- armazenamento seguro em cloud;
- validação clínica e regulatória antes de qualquer modelo de IA.

## Autora

Catarina Sonsine
