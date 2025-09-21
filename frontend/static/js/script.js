document.addEventListener('DOMContentLoaded', function() {

    const pickForMeButton = document.getElementById('pick-for-me-button');
    const findMyHomeButton = document.getElementById('find-my-home-button');
    const findMyHomeButton2 = document.getElementById('find-my-home-button-2');
    const backButton = document.getElementById('back-button');
    const neighborhoodList = document.getElementById('neighborhood-list'); // Define it here

    function updateButtonState() {
        if (neighborhoodList && neighborhoodList.value === '') {
            findMyHomeButton.classList.add('opacity-50', 'cursor-not-allowed');
            findMyHomeButton.classList.remove('hover:bg-green-700', 'cursor-pointer');
            findMyHomeButton.disabled = true;
        } else {
            findMyHomeButton.classList.remove('opacity-50', 'cursor-not-allowed');
            findMyHomeButton.classList.add('hover:bg-green-700', 'cursor-pointer');
            findMyHomeButton.disabled = false;
        }
    }

    if (pickForMeButton) {
        pickForMeButton.addEventListener('click', function() {
            window.location.href = "/find";
        });
    }

    if (findMyHomeButton) {
        findMyHomeButton.addEventListener('click', function(event) {
            if (neighborhoodList && neighborhoodList.value === '') 
            {
                event.preventDefault();
            } 
            else 
            {
                const form = findMyHomeButton.closest('form');
                if (form) 
                {
                    form.submit();
                } 
                else 
                {
                    window.location.href = "/results";
                }
            }
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

    if (neighborhoodList) {
        neighborhoodList.addEventListener('change', updateButtonState);
        updateButtonState();
    }
});