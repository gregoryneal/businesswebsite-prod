let faq_bodies = [];
let canToggleFAQ = true;
let isAnimating = false;

document.addEventListener("DOMContentLoaded", () => { 
    // Set up event listeners for faq buttons
    // .faq-entry classes are the buttons that we click to expand the faq
    let fe = document.getElementsByClassName("faq-entry");
    for (let i = 0; i < fe.length; i++) {

        fe[i].addEventListener('transitionend', () => { 
            isAnimating = false; 
            return false; // cancel any bubbling
        });
        // Get this up here so we can add to faq_bodies 
        // outside of event listener
        let fb = fe[i].getElementsByClassName('faq-body');
        if (fb != null && fb.length > 0) {
            // ... is the spread operator
            // it turns .push(...[1, 2, 3]);
            // into     .push(1, 2, 3);
            faq_bodies.push(...fb);

            fe[i].addEventListener('click', () => {
                // Add the display: block to the .faq-body to trigger the animation
                for (let j = 0; j < fb.length; j++) {
                    //fb[i].style.display = "block";
                    if (canToggleFAQ) {
                        fb[j].classList.toggle('show');
                        //lockFAQ();
                    }
                }
                clickFAQ(fe[i]); // Makes the icon do a spinny animation
            });
        }
    }
});

function closeAllFAQs(except) {
    if (faq_bodies.length > 0) {
        for (let i = 0; i < faq_bodies.length; i++) {
            faq_bodies[i].classList.remove('show');
        }
    }
}

function lockFAQ() {
    canToggleFAQ = false;
    delay(() => {
        canToggleFAQ = true;
    }, 10000);
}

// Animate open/close icon
function clickFAQ(element) {
    let a = element.querySelector(".x-visible");
    let b = element.querySelector(".x-invisible");

    if (!isAnimating) {
        element.classList.toggle('bc');
        a.classList.toggle('a');
        b.classList.toggle('b');
        isAnimating = true;
    }
}

