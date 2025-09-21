document.addEventListener('DOMContentLoaded', function() {

    const pickForMeButton = document.getElementById('pick-for-me-button');
    const findMyHomeButton = document.getElementById('find-my-home-button');
    const findMyHomeButton2 = document.getElementById('find-my-home-button-2');
    const backButton = document.getElementById('back-button');

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

    if (findMyHomeButton2) {
        findMyHomeButton2.addEventListener('click', function() {
            window.location.href = "/results";
        });
    }

    if (backButton) {
        backButton.addEventListener('click', function() {
            window.location.href = "/";
        });
    }
});

