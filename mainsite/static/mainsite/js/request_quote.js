// When the user uploads images in the request form, we need to add the image names to our
// label since we've hidden the actual upload prompt which displays the file names by default
function imagesUploaded() {
    let filesList = document.querySelector("#quote-form-images").files;
    let l = document.querySelector('#uploaded-image-list');
    let newName = "";

    if (filesList.length > 2) {
        newName = filesList.length.toString() + " images"
    } 
    else {
        for (i = 0; i <= filesList.length-1; i++) {
            newName += filesList.item(i).name;
            if (i != filesList.length-1) {
                newName += ", "
            }
        }
    }
    l.innerHTML = newName;
}

function removeImages() {
    let filesList = document.getElementById("quote-form-images");
    let nameList = document.getElementById("uploaded-image-list");
    let newName = "No images uploaded";

    filesList.value = "";
    nameList.innerHTML = newName;
}