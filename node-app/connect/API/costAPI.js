document.getElementById('City-Choices').addEventListener('change', function () {
    const selectedCitys = this.value;

    fetch(`http://127.0.0.1:5001/api/data/${selectedCitys}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('City not found');
            }
            return response.json();
        })
        .then(data => {
            addValuesCost(data);
            console.log('Data retrieved:', data);
        })
        .catch(error => console.error('Error fetching data:', error));
});

function addValuesCost(result) {
    // Extract the 'price' field from each entry
    const priceRange = result.map(entry => entry.price); 
    console.log(priceRange);

    PieChartDataCost.labels = priceRange;

    // Assuming you want to use the percentages too, here's how you can extract them:
    const percentage = result.map(entry => entry.percentage);
    PieChartDataCost.datasets[0].data = percentage;

    costgraphChart.update();
}
