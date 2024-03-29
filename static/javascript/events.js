
function updateRaincheckStatus() {
    let ACTIVE = 1;
    let INACTIVE = 0;
    let events = document.querySelectorAll("div.events");
    events.forEach(event => {
        let eventId = event.dataset.eventId;
        let eventStatus = parseInt(event.dataset.eventStatus);
        if (eventStatus == ACTIVE) {
            let url = '/api/events/' + eventId;
            fetch(url)
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    console.log(data);
                    let updatedStatus = data.status;
                    if (eventStatus !== updatedStatus) {
                        event.querySelector("p.event-status-message").textContent = "HELLO! This event has just been rainchecked!";
                        event.querySelector("p.invitation-status").textContent = "";
                        event.dataset.eventStatus = INACTIVE;
                        let alertModal = new bootstrap.Modal(document.getElementById("reg-modal"));
                        alertModal.show();
                    }
                })
                .catch(function (err) {
                    console.log("Something went wrong.")
                });
        }
    });
}


window.addEventListener('load', function () {
    let fetchInterval = 10000;
    setInterval(updateRaincheckStatus, fetchInterval);
});
