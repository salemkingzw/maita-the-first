document.addEventListener('DOMContentLoaded', function () {
    const countrySelect = document.getElementById('id_country');
    const locationSelect = document.getElementById('id_location');

    countrySelect.addEventListener('change', function () {
        const countryId = this.value;

        if (!countryId) {
            locationSelect.innerHTML = '<option value="">Select location</option>';
            return;
        }

        const url = `/get-location/${countryId}/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                locationSelect.innerHTML = '<option value="">REQUIRED!</option>';
                data.locations.forEach(function (location) {
                    const option = document.createElement('option');
                    option.value = location.id;
                    option.textContent = location.name;
                    locationSelect.appendChild(option);
                });
            });
    });
});