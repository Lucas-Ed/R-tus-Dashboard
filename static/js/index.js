document.addEventListener('DOMContentLoaded', () => {
    // --- Elementos principais ---
    const formReceita = document.getElementById('form-receita');
    const listaIngredientesDiv = document.getElementById('lista-ingredientes');
    const btnAddIngrediente = document.getElementById('btn-add-ingrediente');
    const tabelaReceitas = document.getElementById('tabela-receitas');

    const modalEditarReceitaEl = document.getElementById('modal-editar-receita');
    const bsModalEditarReceita = new bootstrap.Modal(modalEditarReceitaEl);
    const editarConteudoDiv = document.getElementById('editar-conteudo');

    const API_BASE = '/dashboard/';

    // Botão Dashboard
    document.getElementById('btn-open-dashboard').addEventListener('click', (e) => {
    const url = e.target.dataset.url;
    window.location.href = url;
});


    // Função para obter o valor do cookie CSRF
    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

    // --- Funções auxiliares ---
const api = {
    async get(url) {
        const res = await fetch(API_BASE + url);
        if (!res.ok) throw new Error('Erro GET ' + url);
        return res.json();
    },
    async post(url, data) {
        const res = await fetch(API_BASE + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const errText = await res.text();
            console.error('POST error:', errText);
            throw new Error('Erro POST ' + url);
        }
        return res.json();
    },
    async put(url, data) {
        const res = await fetch(API_BASE + url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Erro PUT ' + url);
        return res.json();
    },
    async delete(url) {
        const res = await fetch(API_BASE + url, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': csrftoken }
        });
        if (!res.ok) throw new Error('Erro DELETE ' + url);
        return true;
    }
};

    function escapeHtml(text) {
        if (!text) return '';
        return text.replace(/[&<>"'`]/g, m => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;', '`': '&#96;'
        })[m]);
    }

    // ==================== INGREDIENTES UI/ Modal editar ====================
    function createIngredienteElement(ingrediente = null) {
        const id = ingrediente && ingrediente._id ? ingrediente._id : `ing-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
        const wrapper = document.createElement('div');
        wrapper.className = 'ingrediente-item';
        wrapper.dataset.ingId = id;

        wrapper.innerHTML = `
            <div class="row align-items-center">
                <div class="col-12 col-md-5 mb-2">
                    <label class="form-label small">Alimento</label>
                    <input type="text" 
                        class="form-control form-control-sm ing-nome" 
                        value="${ingrediente ? escapeHtml(ingrediente.alimento || ingrediente.nome || '') : ''}" 
                        required>
                </div>
                <div class="col-4 col-md-2 mb-2">
                    <label class="form-label small">Peso bruto</label>
                    <input type="number" step="0.01" 
                        class="form-control form-control-sm ing-peso-bruto" 
                        value="${ingrediente ? ingrediente.peso_bruto || '' : ''}">
                </div>
                <div class="col-4 col-md-2 mb-2">
                    <label class="form-label small">Peso líquido</label>
                    <input type="number" step="0.01" 
                        class="form-control form-control-sm ing-peso-liq" 
                        value="${ingrediente ? ingrediente.peso_liquido || '' : ''}">
                </div>
                <div class="col-4 col-md-2 mb-2">
                    <label class="form-label small">Peso processado</label>
                    <input type="number" step="0.01" 
                        class="form-control form-control-sm ing-peso-proc" 
                        value="${ingrediente ? ingrediente.peso_processado || '' : ''}">
                </div>
                <div class="col-12 col-md-1 mb-2 text-end">
                    <button type="button" class="btn btn-sm btn-danger btn-delete-ing">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `;

        wrapper.querySelector('.btn-delete-ing').addEventListener('click', () => wrapper.remove());
        return wrapper;
    }

    btnAddIngrediente.addEventListener('click', () => {
        listaIngredientesDiv.appendChild(createIngredienteElement());
    });

    function getIngredientesFromUI(container = listaIngredientesDiv) {
        return Array.from(container.querySelectorAll('.ingrediente-item')).map(it => ({
            nome: it.querySelector('.ing-nome').value.trim(),
            peso_bruto: parseFloat(it.querySelector('.ing-peso-bruto').value) || 0,
            peso_liquido: parseFloat(it.querySelector('.ing-peso-liq').value) || 0,
            peso_processado: parseFloat(it.querySelector('.ing-peso-proc').value) || 0,
        }));
    }

    // ==================== RECEITAS ====================
    // Função para renderizar a tabela de receitas
    async function renderReceitasTable() {
        try {
            const receitas = await api.get('receitas/');
            tabelaReceitas.innerHTML = '';

            receitas.forEach((r, idx) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${idx + 1}</td>
                    <td>${escapeHtml(r.nome)}</td>
                    <td>${escapeHtml(r.categoria || '')}</td>
                    <td>${r.porcao_individual || 0} ${r.medida || ''}</td>
                    <td>
                        <button class="btn btn-sm btn-primary btn-edit" data-id="${r._id}"><i class="bi bi-pencil"></i></button>
                        <button class="btn btn-sm btn-danger btn-delete" data-id="${r._id}"><i class="bi bi-trash"></i></button>
                    </td>
                `;
                tabelaReceitas.appendChild(tr);

                tr.querySelector('.btn-edit').addEventListener('click', () => openEditarReceitaModal(r._id || r.id));
                tr.querySelector('.btn-delete').addEventListener('click', () => confirmarExclusaoReceita(r._id || r.id));

            });
        } catch (err) {
            console.error('Erro ao carregar receitas', err);
        }
    }
    // Função para confirmar e excluir uma receita
    async function confirmarExclusaoReceita(id) {
        const result = await Swal.fire({
            title: 'Excluir receita?',
            text: 'Deseja realmente excluir esta receita?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sim, excluir',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#d9534f'
        });
        if (result.isConfirmed) {
            await api.delete(`receitas/${id}/`);
            Swal.fire('Excluída', 'Receita removida com sucesso.', 'success');
            renderReceitasTable();
        }
    }
    // ==================== SALVAR NOVA RECEITA ====================
    formReceita.addEventListener('submit', async (e) => {
        e.preventDefault();

        const id = document.getElementById('receita-id').value;
        const data = {
            nome: document.getElementById('receita-nome').value.trim(),
            categoria: document.getElementById('receita-categoria').value.trim(),
            porcao_individual: parseFloat(document.getElementById('receita-porcao').value) || 0,
            medida: document.getElementById('receita-medida').value,
            modo_preparo: document.getElementById('receita-modo').value.trim(),
            ingredientes: getIngredientesFromUI()
        };

        try {
            if (id) {
                await api.put(`receitas/${id}/`, data);
                Swal.fire('Atualizado', 'Receita atualizada com sucesso.', 'success');
            } else {
                await api.post('receitas/', data);
                Swal.fire('Salvo', 'Receita criada com sucesso.', 'success');
            }
            formReceita.reset();
            listaIngredientesDiv.innerHTML = '';
            renderReceitasTable();
        } catch (err) {
            Swal.fire('Erro', 'Falha ao salvar receita.', 'error');
        }
    });

    // ==================== EDITAR RECEITA ====================
    async function openEditarReceitaModal(receitaId) {
        try {
            const r = await api.get(`receitas/${receitaId}/`);
            editarConteudoDiv.innerHTML = '';

            const clone = formReceita.cloneNode(true);
            clone.querySelector('#receita-id').value = r._id || r.id;
            clone.querySelector('#receita-nome').value = r.nome;
            clone.querySelector('#receita-categoria').value = r.categoria;
            clone.querySelector('#receita-porcao').value = r.porcao_individual;
            clone.querySelector('#receita-medida').value = r.medida;
            clone.querySelector('#receita-modo').value = r.modo_preparo;

            const listaClone = clone.querySelector('#lista-ingredientes');
            listaClone.innerHTML = '';
            (r.ingredientes || []).forEach(ing => {
                listaClone.appendChild(createIngredienteElement(ing));
            });
            // Reanexa o evento de adicionar ingrediente no modal
            const btnAddIngredienteClone = clone.querySelector('#btn-add-ingrediente');
            if (btnAddIngredienteClone) {
                btnAddIngredienteClone.addEventListener('click', () => {
                    listaClone.appendChild(createIngredienteElement());
                });
            }

            clone.addEventListener('submit', async ev => {
                ev.preventDefault();
                const data = {
                    nome: clone.querySelector('#receita-nome').value.trim(),
                    categoria: clone.querySelector('#receita-categoria').value.trim(),
                    porcao_individual: parseFloat(clone.querySelector('#receita-porcao').value) || 0,
                    medida: clone.querySelector('#receita-medida').value,
                    modo_preparo: clone.querySelector('#receita-modo').value.trim(),
                    ingredientes: getIngredientesFromUI(listaClone)
                };
                await api.put(`receitas/${receitaId}/`, data);
                bsModalEditarReceita.hide();
                Swal.fire('Atualizado', 'Receita atualizada com sucesso.', 'success');
                renderReceitasTable();
            });

            editarConteudoDiv.appendChild(clone);
            bsModalEditarReceita.show();
        } catch (err) {
            Swal.fire('Erro', 'Falha ao carregar receita.', 'error');
        }
    }

    // ==================== Inicialização ====================
    renderReceitasTable();
});