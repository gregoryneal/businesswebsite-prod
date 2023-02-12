function doneCallback(solution) {
    console.log("Captcha finished")

    var submitButton = document.querySelector("#quote-submit");
    submitButton.attributes.removeNamedItem('disabled');
}