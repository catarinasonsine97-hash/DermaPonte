# Trabalhar no DermaPonte

O MVP Django permanece na raiz. O novo serviço Java e sua interface estão em `backend-java/`.

```powershell
git clone https://github.com/catarinasonsine97-hash/DermaPonte.git
cd DermaPonte
git switch -c feat/nome-da-alteracao
```

Execute os testes da tecnologia alterada antes de registrar o trabalho. No Java, use JDK 21 e Maven: `cd backend-java`, `mvn test`. Para execução, defina `DERMAPONTE_PASSWORD` apenas no ambiente e use `mvn spring-boot:run`. A porta padrão é 8080; defina `SERVER_PORT=8081` se necessário. `local.ps1` exige ferramentas portáteis em `.tools`, não fornecidas no Git.

Abra `backend-java` como pasta do VS Code para usar a configuração de debug. Ajuste a referência ao JDK local em `launch.json` ou configure o runtime Java na sua máquina. Não registre senhas, fotos, banco local, `.tools`, `target` ou configurações específicas do computador.

```powershell
git status
git add caminho/do/arquivo
git diff --cached
git commit -m "feat: descreva a alteracao"
git push -u origin feat/nome-da-alteracao
```

Abra um pull request para revisão. Atualize a documentação quando mudar o fluxo. Não reescreva o histórico compartilhado nem use push forçado. O protótipo é educacional e não deve receber dados reais de pacientes.
