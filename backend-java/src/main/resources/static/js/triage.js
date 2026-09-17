'use strict';
const form = document.querySelector('#triage');
const feedback = document.querySelector('#feedback');
const submit = document.querySelector('#submit');
const connection = document.querySelector('#connection');
csrf().then(() => { connection.textContent = '● API Java conectada'; })
  .catch(() => { connection.textContent = 'API indisponível ou sessão expirada'; });
async function csrf() {
  const response = await fetch('/api/v1/session/csrf', {headers: {'Accept': 'application/json'}});
  if (response.redirected || response.status === 401) throw new Error('Sua sessão terminou. Acesse /login e entre novamente.');
  if (!response.ok) throw new Error('Não foi possível preparar o envio. Tente novamente.');
  return response.json();
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  submit.disabled = true;
  document.querySelector('#reset').disabled = true;
  form.setAttribute('aria-busy', 'true');
  feedback.textContent = 'Calculando prioridade demonstrativa…';
  document.querySelector('#result').hidden = true;
  try {
    const token = await csrf();
    const data = {};
    for (const name of ['changed','bleeding','itchingOrPain','notHealing','personalHistory','familyHistory']) data[name] = form.elements[name].checked;
    const response = await fetch('/api/v1/triage/assessment', {method: 'POST', headers: {'Content-Type':'application/json', 'Accept':'application/json', [token.headerName]:token.token}, body:JSON.stringify(data)});
    if (response.redirected || response.status === 401) throw new Error('Sua sessão terminou. Acesse /login e entre novamente.');
    if (!response.ok) throw new Error('Não foi possível calcular. Verifique sua sessão e tente novamente.');
    const result = await response.json();
    const labels = {URGENT:'Revisão prioritária', SOON:'Revisão breve', ROUTINE:'Revisão de rotina'};
    document.querySelector('#result-title').textContent = labels[result.priority] || 'Prioridade demonstrativa';
    document.querySelector('#score').textContent = `Pontuação demonstrativa: ${result.score}. Não representa probabilidade de doença.`;
    const reasons = document.querySelector('#reasons');
    reasons.replaceChildren();
    for (const reason of result.reasons.length ? result.reasons : ['Nenhum dos sinais do questionário foi marcado. Isso não exclui doença.']) {
      const item = document.createElement('li'); item.textContent = reason; reasons.append(item);
    }
    document.querySelector('#disclaimer').textContent = result.disclaimer;
    const panel = document.querySelector('#result');
    panel.className = `result-card ${result.priority.toLowerCase()}`;
    panel.hidden = false; panel.focus();
    document.querySelector('#placeholder').hidden = true;
    feedback.textContent = 'Cálculo concluído.';
  } catch (error) { feedback.textContent = error.message || 'Falha de conexão. Verifique se o servidor está rodando.'; }
  finally { submit.disabled = false; document.querySelector('#reset').disabled = false; form.setAttribute('aria-busy', 'false'); }
});
document.querySelector('#reset').addEventListener('click', () => {
  form.reset();
  document.querySelector('#result').hidden = true;
  document.querySelector('#placeholder').hidden = false;
  feedback.textContent = 'Respostas limpas. Você pode testar outro cenário fictício.';
  form.elements.changed.focus();
});
document.querySelector('#logout').addEventListener('click', async () => {
  try {
    const token = await csrf();
    const response = await fetch('/logout', {method:'POST', headers:{[token.headerName]:token.token}});
    if (!response.ok) throw new Error('Não foi possível sair. Tente novamente.');
    window.location.assign('/login?logout');
  } catch (error) { feedback.textContent = error.message; }
});
