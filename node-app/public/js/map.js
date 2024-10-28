const width = 960;
const height = 500;

const svg = d3.select("#map")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

const projection = d3.geoMercator()
    .center([-106, 56]) // Center around Canada
    .translate([width / 2, height / 2])
    .scale(3000); // Scale can be adjusted

const path = d3.geoPath().projection(projection);

// Load the GeoJSON data for Canada
d3.json('https://raw.githubusercontent.com/johan/world.geo.json/master/countries/CAN.geo.json')
    .then(data => {
        svg.selectAll("path")
            .data(data.features)
            .enter().append("path")
            .attr("d", path)
            .attr("fill", "#69b3a2") // Color of the map
            .attr("stroke", "#fff")
            .attr("stroke-width", 1);
    })
    .catch(error => {
        console.error("Error loading the GeoJSON data: ", error);
    });
