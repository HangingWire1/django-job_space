// Function to handle dependent dropdowns
function initializeDependentDropdown(sourceId, targetId, url) {
    const sourceElem = document.getElementById(sourceId);
    const targetElem = document.getElementById(targetId);

    if (sourceElem && targetElem) {
        sourceElem.addEventListener("change", function() {
            const val = this.value;
            fetch(`${url}?state_id=${val}`)
                .then(response => response.text())
                .then(data => {
                    targetElem.innerHTML = data;
                })
                .catch(error => console.error('Error loading dropdown:', error));
        });
    }
}