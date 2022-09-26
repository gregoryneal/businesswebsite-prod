let t = 500;

function showRegisterForm(){
    let l = document.getElementById("login-body");
    let r = document.getElementById("register-body");

    if (l != null && r != null) {
        l.classList.remove('show');
        l.addEventListener('transitionend', ()=>{
            l.style.display = "none";
            r.style.display = "block";
            r.classList.add('show');
        }, {once:true});
    }    
}

function showLoginForm(){
    let l = document.getElementById("login-body");
    let r = document.getElementById("register-body");

    if (l != null && r != null) {
        r.classList.remove('show');
        r.addEventListener('transitionend', ()=>{
            r.style.display = "none";
            l.style.display = "block";
            l.classList.add('show');
        }, {once:true});
    }
}