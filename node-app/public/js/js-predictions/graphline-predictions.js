
// Line Chart Data: Random CO2 Emissions for Daily Line Chart (for each city)
const dailyLineChartData = {
    labels: ["2023-02-24", "2023-02-26", "2023-03-01", "2023-03-23", "2023-03-24", "2023-03-25"],
     datasets: [{
        label: "Prediction",
        data: [, , , , ,420.14317416759800],// Align
        borderColor: //orange color for prediction 
        'rgb(255,0,0,1)',
        borderDash: [20, 30],
        pointBackgroundColor: "transparent"
    },{
        label: "Ontario",
        data: [419.6575297941606, 409.7299041666667, 419.824341, 419.7805289008265, 422.181091, 420.14317416759775,,], //Default dataset
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        pointBackgroundColor: "transparent"
    }]
};


const config1 ={
    type: 'line',
    data: dailyLineChartData,
    options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
            x: {
                type: 'category',  // Use 'category' instead of 'time' for string labels
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'CO2 Emission (tons)'
                },
                ticks:{
                    stepSize: 0.00025,
                }

            }
        },
        plugins:{
            title:{
                display: true,
                text: 'Co2 Analysis and Prediction'
            }
        }
    },
};


const graphChart = new Chart(
    document.getElementById('co2Predisction'),
    config1
);
