document.addEventListener('DOMContentLoaded', function() {
    
    const pickForMeButton = document.getElementById('pick-for-me-button');
    const findMyHomeButton = document.getElementById('find-my-home-button');

    if (pickForMeButton) {
        pickForMeButton.addEventListener('click', function() {
            window.location.href = "/find";
        });
    }

    if (findMyHomeButton) {
        findMyHomeButton.addEventListener('click', function() {
            window.location.href = "/results";
        });
    }
});