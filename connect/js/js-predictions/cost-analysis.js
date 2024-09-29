
// Line Chart Data: Random CO2 Emissions for Daily Line Chart (for each city)
const PieChartDataCost = {
    labels: ["$2,000-$1,000", "$200-$100", "$20-$10"],
    datasets: [{
        data: [20,30,50],
        backgroundColor: [
            'rgb(255, 99, 132,0.5)',
            'rgb(54, 162, 235,0.5)',
            'rgb(255, 205, 86,0.5)'
        ],
        borderColor:[
            'rgb(255, 99, 132,1)',
            'rgb(54, 162, 235,1)',
            'rgb(255, 205, 86,1)'
        ],
        pointBackgroundColor: "transparent"
    }]
};

const config2 = {
    type: 'pie',
    data: PieChartDataCost,
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Cost Analysis'
            }
        }
    }
};


const costgraphChart = new Chart(
    document.getElementById('costLinechart'),
    config2
);
