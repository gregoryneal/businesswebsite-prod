function setCookie(cname, cvalue, mins) {
    let maxage = "max-age="+(mins * 60).toString();
    document.cookie = cname + "=" + cvalue + ";" + maxage + ";path=/";
  }
  
function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkCookie(cname) {
  let cookie = getCookie(cname);
  if (cookie != "") {
      //console.log("Cookie exists!");
      return true;
  } else {
      //console.log("Cookie doesn't exist!");
      return false;
  }
}

function deleteCookie(cname) {
  setCookie(cname, "", -1);
}