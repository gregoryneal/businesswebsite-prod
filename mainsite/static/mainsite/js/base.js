// Toggler objects {button: buttonElem, content: contentElem}
let togglers = []
let oldWidth = -632;

document.addEventListener("DOMContentLoaded", () => { 

    // IntersectionObserver API stuff
    // Triggering animations when elements are scrolled into view etc.
    // Select all .easeload-ltr and .easeload-rtl
    let easeloadltr = document.querySelectorAll('.easeload-ltr');
    let easeloadrtl = document.querySelectorAll('.easeload-rtl');
    // THIS FUNCTION GETS CALLED WHENEVER A ELEMENT (OR ELEMENTS) COME INTO OR GO OUT OF VIEW
    function callback (observations, observer) {
        observations.forEach(observation => {
            if (observation.isIntersecting) { //IF IT'S IN VIEW
                observation.target.classList.add('animate');
            }
            else {
                // when the element is not in view
                //observation.target.classList.remove('animate');
            }      
        });
    }
      
    // CREATE AN INTERSECTION OBSERVER
    let options = {
        root: null, //null means it will observe on the viewport
        rootMargin: '0px',
        threshold: .01 //1 means the whole element needs to be viewable before we animate it
    }

    let observer = new IntersectionObserver(callback, options);
    
    // NOW PUT THE OBSERVER ON EACH OF THE ELEMENTS WE WANT TO ANIMATE WHEN IT'S IN VIEW
    for (let i=0; i< easeloadltr.length; i++) {
        observer.observe(easeloadltr[i]); 
    }
    for (let i=0; i< easeloadrtl.length; i++) {
        observer.observe(easeloadrtl[i]); 
    }
   

    // Login modal and show buttons
    let lmt = document.getElementsByClassName("show-login-modal");
    let lm = document.getElementById("login-modal");
    // Login modal close buttons
    let lmc = document.getElementsByClassName("hide-login-modal");

    
    let pm_button = document.getElementById("profile-menu-button");
    let pm_content = document.getElementById("profile-menu-content");
    if (pm_content == null) pm_content = document.getElementById("admin-menu-content");
    let st_button = document.getElementById("sidebar-toggler-outer");
    let st_content = document.getElementById("sidebar");
    let dimmer = document.getElementById("dimmer");

    let sm_button = document.getElementById("sidebar-profile-menu-label");
    let sm_content = document.getElementById("sidebar-profile-menu-content");
    if (sm_content == null) sm_content = document.getElementById("sidebar-admin-menu-content");

    if (pm_button != null && pm_content != null) {
        togglers.push(GetToggler(pm_button, pm_content));
    }

    if (sm_button != null && sm_content != null) {
        togglers.push(GetToggler(sm_button, sm_content));
    }

    togglers.push(GetToggler(st_button, st_content));
    togglers.push(GetToggler(st_button, dimmer)); // Include this so togglers will automatically remove the class

    let nt = document.querySelector("#navigation-tabs a[href='" + window.location.pathname + "']");
    if (nt != null) {
        nt.classList.add("active");
    }

    window.addEventListener('resize', () => {        
        let width = window.innerWidth;

        // -632 is the default value that I set for
        // this variable to indicate that it has not
        // been set yet. NO special significance.
        if (oldWidth == -632) {
            oldWidth = width;
        }

        // We have expanded beyond 992 px width
        if (oldWidth <= 992 && width > 992) {
            closeLoginModal();
            closeSidebar();
            hideDimmer();
        }

        oldWidth = width;
    
    }, true);

    if (lm != null) {
        // assign open login modal event listeners
        for (let i = 0; i < lmt.length; i++) {
            lmt[i].addEventListener('click', (e) => {
                closeSidebar();
                openLoginModal();
                e.stopPropagation();
            });
        }

        // close login modals event listeners
        for (let i = 0; i < lmc.length; i++) {
            lmc[i].addEventListener('click', () => {
                closeLoginModal();
            });
        }
    }

    // Sidebar profile menu button event listeners
    if (sm_button != null) {
        sm_button.addEventListener('click', () => {
            if (sm_content != null) {
                sm_content.classList.toggle('show');
            }

            if (pm_content != null) {
                pm_content.classList.remove('show');
            }
        });
    }

    // Profile menu button event listeners
    if (pm_button != null) {
        pm_button.addEventListener('click', () => {
            if (pm_content != null) {
                pm_content.classList.toggle('show');
            }
            closeSidebar();
        });
    }
    
    // Sidebar toggler event listeners
    st_button.addEventListener('click', (e) => {
        toggleSidebar();
        if (pm_content != null) {
            pm_content.classList.remove('show');
        }
        console.log("toggled content " + e.target.id);
        e.stopPropagation(); //prevents event from propagating to the window where it will be received by click and then st_content will be hidden again
    });

    document.getElementById("close-sidebar").addEventListener('click', (e) => {
        closeSidebar();
        hideDimmer();
        e.stopPropagation();
    });

    dimmer.addEventListener('click', () => {
        closeSidebar();
        closeLoginModal();
    });
});

function GetToggler(button, content) {
    return {
        button: button,
        content: content
    }
}

function closeToggler(toggler) {
    toggler.content.classList.remove('show');
}

function openLoginModal() {    
    let lm = document.getElementById("login-modal");
    if (lm != null) {
        showDimmer();
        lm.style.display = "flex";
    }
}

function closeLoginModal() {    
    hideDimmer();
    let lm = document.getElementById("login-modal");
    if (lm != null) {
        lm.style.display = "none";
    }
}

function openSidebar() {    
    let st_content = document.getElementById("sidebar");
    
    if (st_content != null) {
        st_content.style.display = "block";
    }
}

function closeSidebar() {
    let st_content = document.getElementById("sidebar");
    let sm_content = document.getElementById("sidebar-profile-menu-content");

    if (sm_content != null) {        
        sm_content.classList.remove('show');
    }

    if (st_content != null) {
        st_content.style.display = "none";
    }
}

//Controls the dimmer as well, use sparingly
function toggleSidebar() {
    let st_content = document.getElementById("sidebar");

    if (st_content != null) {
        if (st_content.classList.contains('show')) {
            closeSidebar();
            st_content.addEventListener('transitionend', hideDimmer(), {once:true});
        } else {
            showDimmer();
            st_content.addEventListener('transitionend', openSidebar(), {once:true});
        }
    }
}

function showDimmer() {    
    let dimmer = document.getElementById("dimmer");
    if (dimmer != null) {  
        dimmer.style.display = "block";
        dimmer.classList.add('show');
    }
}

function hideDimmer() {    
    let dimmer = document.getElementById("dimmer");
    if (dimmer != null) {
        dimmer.classList.remove('show');
        dimmer.style.display = "none";
    }
}

function contains(array, obj) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] === obj) {
            return true;
        }
    }
    return false;
}

function isChild(obj, parentObj){
    while (obj != undefined && obj != null && obj.tagName.toUpperCase() != 'BODY'){
        if (obj == parentObj){
            return true;
        }
        obj = obj.parentNode;
    }
    return false;
}


// https://stackoverflow.com/questions/1909441/how-to-delay-the-keyup-handler-until-the-user-stops-typing?rq=1
function delay(callback, ms) {
    var timer = 0;
    return function() {
      var context = this;
      var args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        callback.apply(context, args);
      }, ms || 0);
    };
}