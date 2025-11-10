   document.addEventListener("DOMContentLoaded", async () => {
    const apiUrl = "/dashboard/dashboard-stats/";

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        if (data.error) throw new Error(data.error);

        // Atualiza indicadores numéricos
        document.getElementById("total-receitas").textContent = data.total_receitas || 0;
        document.getElementById("total-ingredientes").textContent = data.total_ingredientes || 0;
        document.getElementById("media-energia").textContent = data.media_energia ? data.media_energia.toFixed(2) : "0";

        // === Gráfico: Receitas por Tipo ===
        const tiposLabels = Object.keys(data.receitas_por_tipo || {});
        const tiposData = Object.values(data.receitas_por_tipo || {});

        new Chart(document.getElementById("chartTipos"), {
            type: 'pie',
            data: {
                labels: tiposLabels.length ? tiposLabels : ["Sem dados"],
                datasets: [{
                    data: tiposData.length ? tiposData : [1],
                    backgroundColor: ['#4aad9d', '#ff6384', '#36a2eb', '#ffcd56', '#9966ff', '#c9cbcf']
                }]
            },
            options: { plugins: { legend: { position: 'bottom' } } }
        });

        // === Gráfico: Energia Média por Receita (ou indicador alternativo) ===
        new Chart(document.getElementById("chartEnergia"), {
            type: 'bar',
            data: {
                labels: ['Energia Média (kcal/100g)'],
                datasets: [{
                    label: 'Energia Média',
                    data: [data.media_energia],
                    backgroundColor: '#4aad9d'
                }]
            },
            options: {
                scales: { y: { beginAtZero: true } },
                plugins: { legend: { display: false } }
            }
        });

        // === Gráfico: Top 5 Ingredientes Mais Usados ===
        const ingLabels = Object.keys(data.top_ingredientes || {});
        const ingData = Object.values(data.top_ingredientes || {});

        new Chart(document.getElementById("chartIngredientes"), {
            type: 'doughnut',
            data: {
                labels: ingLabels.length ? ingLabels : ["Sem dados"],
                datasets: [{
                    data: ingData.length ? ingData : [1],
                    backgroundColor: ['#4aad9d', '#36a2eb', '#ff6384', '#ffcd56', '#9966ff']
                }]
            },
            options: { plugins: { legend: { position: 'bottom' } } }
        });

    } catch (error) {
        console.error("Erro ao carregar dashboard:", error);
    }
});
   //    // Exemplos de dados estáticos
    //     const ctx1 = document.getElementById('chartTipos');
    //     new Chart(ctx1, {
    //         type: 'pie',
    //         data: {
    //             labels: ['Doce', 'Salgada', 'Vegana', 'Fit'],
    //             datasets: [{ data: [5, 8, 2, 3], backgroundColor: ['#4aad9d', '#ff6384', '#36a2eb', '#ffcd56'] }]
    //         }
    //     });

    //     const ctx2 = document.getElementById('chartEnergia');
    //     new Chart(ctx2, {
    //         type: 'bar',
    //         data: {
    //             labels: ['Receita A', 'Receita B', 'Receita C'],
    //             datasets: [{ label: 'Energia (kcal/100g)', data: [230, 180, 320], backgroundColor: '#4aad9d' }]
    //         }
    //     });

    //     const ctx3 = document.getElementById('chartIngredientes');
    //     new Chart(ctx3, {
    //         type: 'doughnut',
    //         data: {
    //             labels: ['Farinha', 'Açúcar', 'Ovos', 'Leite', 'Manteiga'],
    //             datasets: [{ data: [10, 8, 7, 6, 5], backgroundColor: ['#4aad9d', '#36a2eb', '#ff6384', '#ffcd56', '#9966ff'] }]
    //         }
    //     });