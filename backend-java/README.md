# DermaPonte — backend Java (primeira etapa)

API independente do MVP Django. Java 21, Spring Boot 3.5 e Maven.

Esta etapa implementa o cálculo demonstrativo de prioridade com explicações, validação de campos e proteção padrão do Spring Security. A página inicial adapta o visual do MVP Django e envia o questionário à API com o token CSRF da sessão. Não analisa imagens, não realiza diagnóstico e não substitui avaliação médica. Nenhuma informação de paciente é persistida.

## Executar

Com JDK 21 e Maven instalados:

```powershell
$env:DERMAPONTE_PASSWORD = 'escolha-uma-senha-local-forte'
mvn test
mvn spring-boot:run
```

O serviço escuta somente em `127.0.0.1:8080`. O usuário local é `developer`. Nunca publique senhas. A proteção CSRF padrão permanece ativa; um cliente POST deve autenticar e enviar o token CSRF.

Com as ferramentas portáteis disponíveis em `.tools`, use `./local.ps1 test` e `./local.ps1 run` no PowerShell, definindo antes a senha conforme acima.

Abra `http://127.0.0.1:8080/`, faça login e preencha o questionário. A interface reutiliza o CSS do MVP e adapta seus templates para HTML/JavaScript. Fotos, contas de pacientes, revisão clínica e agenda ainda não estão implementadas em Java. Use apenas exemplos fictícios.

A tela possui indicador de conexão, questionário, painel de resultado com pontuação e motivos, estado de carregamento e botão para limpar as respostas. O resultado não é salvo. Após editar os arquivos, reinicie o servidor e atualize o navegador com Ctrl+F5.

Para conferir manualmente: nenhum sinal marcado retorna pontuação 0 e revisão de rotina; apenas mudança retorna 3 e revisão breve; mudança e sangramento retornam 6 e revisão prioritária. Essas categorias são exclusivamente demonstrativas.

## Depurar no VS Code

Abra esta pasta como raiz do workspace e instale a extensão recomendada **Extension Pack for Java**. Aguarde a importação Maven terminar. Pare qualquer execução anterior na porta 8080, selecione **DermaPonte — Debug local** em Executar e Depurar e pressione F5. Informe uma senha local quando solicitado; ela não é salva no arquivo de configuração. Acesse `/` e entre com `developer` e a senha escolhida. Um breakpoint dentro de `PriorityService.assess` será acionado ao enviar o questionário.

Os arquivos locais `settings.json` e `maven-settings.xml` apontam para as ferramentas desta máquina e são ignorados pelo Git. Se a versão/pasta do JDK mudar, atualize também `javaExec` em `launch.json`. Esta configuração foi criada, mas a sessão interativa de debug ainda não foi verificada.

## Endpoint da triagem

`POST /api/v1/triage/assessment`

```json
{
  "changed": true,
  "bleeding": false,
  "itchingOrPain": false,
  "notHealing": false,
  "personalHistory": false,
  "familyHistory": false
}
```

Retorna `priority`, `score`, `reasons` e `disclaimer`. Todos os seis campos são obrigatórios.

## Próximas etapas

1. Cadastro e autenticação de pacientes/profissionais com permissões e testes de isolamento.
2. PostgreSQL e migrações para casos, revisão clínica e auditoria.
3. Upload privado com validação de imagem, limites e controle de acesso.
4. Agenda com horários, transações e prevenção de reservas simultâneas.
5. Integração gradual com a interface existente.

Não usar com dados reais nesta fase. Regras não validadas clinicamente; IA e uso clínico estão fora do escopo atual.
