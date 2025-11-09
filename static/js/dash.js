       // Exemplos de dados estáticos
        const ctx1 = document.getElementById('chartTipos');
        new Chart(ctx1, {
            type: 'pie',
            data: {
                labels: ['Doce', 'Salgada', 'Vegana', 'Fit'],
                datasets: [{ data: [5, 8, 2, 3], backgroundColor: ['#4aad9d', '#ff6384', '#36a2eb', '#ffcd56'] }]
            }
        });

        const ctx2 = document.getElementById('chartEnergia');
        new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: ['Receita A', 'Receita B', 'Receita C'],
                datasets: [{ label: 'Energia (kcal/100g)', data: [230, 180, 320], backgroundColor: '#4aad9d' }]
            }
        });

        const ctx3 = document.getElementById('chartIngredientes');
        new Chart(ctx3, {
            type: 'doughnut',
            data: {
                labels: ['Farinha', 'Açúcar', 'Ovos', 'Leite', 'Manteiga'],
                datasets: [{ data: [10, 8, 7, 6, 5], backgroundColor: ['#4aad9d', '#36a2eb', '#ff6384', '#ffcd56', '#9966ff'] }]
            }
        });