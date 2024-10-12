async function loadComponent(url, elementId) {
    const response = await fetch(url);
    const text = await response.text();
    document.getElementById(elementId).innerHTML = text;
}
window.onload = () => {
    loadComponent('../structure/navbar.html', 'navbar');
    loadComponent('../structure/footer.html', 'footer');
};
