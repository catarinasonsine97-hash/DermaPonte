# DermaPonte — backend Java (primeira etapa)

API independente do MVP Django. Java 21, Spring Boot 3.5 e Maven.

Esta etapa implementa apenas o cálculo demonstrativo de prioridade com explicações, validação de campos e proteção padrão do Spring Security. Não analisa imagens, não realiza diagnóstico e não substitui avaliação médica. Nenhuma informação de paciente é persistida.

## Executar

Com JDK 21 e Maven instalados:

```powershell
$env:DERMAPONTE_PASSWORD = 'escolha-uma-senha-local-forte'
mvn test
mvn spring-boot:run
```

O serviço escuta somente em `127.0.0.1:8080`. O usuário local é `developer`. Nunca publique senhas. A proteção CSRF padrão permanece ativa; um cliente POST deve autenticar e enviar o token CSRF. A integração com o front-end ainda não está implementada.

## Endpoint

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
