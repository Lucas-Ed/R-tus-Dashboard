const apiBase = '/api/rotulos/';

async function fetchIndicadores() {
    const res = await fetch('/api/indicadores/');
    const data = await res.json();
    document.getElementById('total-rotulos').innerText = data.total_rotulos;
    document.getElementById('avg-energy').innerText = data.avg_energy_kcal_100.toFixed(2);
    // grafico top energy
    const labels = data.top_energy.map(x => x.nome);
    const valores = data.top_energy.map(x => x.energia);
    if (window.topEnergyChart) {
        window.topEnergyChart.data.labels = labels;
        window.topEnergyChart.data.datasets[0].data = valores;
        window.topEnergyChart.update();
    } else {
        const ctx = document.getElementById('topEnergyChart').getContext('2d');
        window.topEnergyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Energia (kcal/100g)',
                    data: valores
                }]
            },
            options: {}
        });
    }
}

async function fetchRotulos() {
    const res = await fetch(apiBase);
    const data = await res.json();
    const tbody = document.getElementById('tabela-rotulos');
    tbody.innerHTML = '';
    data.results.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${r.id}</td>
            <td>${r.nome_receita}</td>
            <td>${r.energia_kcal_100 ?? ''}</td>
            <td>${r.proteinas_g_100 ?? ''}</td>
            <td>${r.sodio_mg_100 ?? ''}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="editRotulo('${r.id}')">Editar</button>
                <button class="btn btn-sm btn-danger" onclick="deleteRotulo('${r.id}')">Excluir</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function createOrUpdateRotulo(payload, id=null) {
    const url = id ? apiBase + id + '/' : apiBase;
    const method = id ? 'PUT' : 'POST';
    const res = await fetch(url, {
        method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    return res.json();
}

async function deleteRotulo(id) {
    if(!confirm('Confirma exclusão?')) return;
    await fetch(apiBase + id + '/', {method: 'DELETE'});
    await refreshAll();
}

async function editRotulo(id) {
    const res = await fetch(apiBase + id + '/');
    const data = await res.json();
    const r = data.result;
    document.getElementById('rotulo-id').value = r.id;
    document.getElementById('nome_receita').value = r.nome_receita;
    document.getElementById('energia_kcal_100').value = r.energia_kcal_100 || '';
    document.getElementById('proteinas_g_100').value = r.proteinas_g_100 || '';
    document.getElementById('sodio_mg_100').value = r.sodio_mg_100 || '';
}

document.getElementById('form-rotulo').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('rotulo-id').value || null;
    const payload = {
        nome_receita: document.getElementById('nome_receita').value,
        energia_kcal_100: parseFloat(document.getElementById('energia_kcal_100').value) || 0,
        proteinas_g_100: parseFloat(document.getElementById('proteinas_g_100').value) || 0,
        sodio_mg_100: parseFloat(document.getElementById('sodio_mg_100').value) || 0,
    };
    await createOrUpdateRotulo(payload, id);
    document.getElementById('form-rotulo').reset();
    document.getElementById('rotulo-id').value = '';
    await refreshAll();
});

document.getElementById('btn-clear').addEventListener('click', () => {
    document.getElementById('form-rotulo').reset();
    document.getElementById('rotulo-id').value = '';
});

async function refreshAll(){
    await fetchRotulos();
    await fetchIndicadores();
}

window.addEventListener('load', async () => {
    await refreshAll();
});