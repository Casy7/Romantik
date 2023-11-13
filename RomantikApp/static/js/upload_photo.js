function readURL() {
    var myimg = document.getElementById("myimg");
    var input = document.getElementById("uploaded_avatar");
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {

            // console.log("changed");
            myimg.src = e.target.result;

            //paste code here
        }
        create_del_button();
        // document.getElementById("del_photo").style.display = "visible";
        reader.readAsDataURL(input.files[0]);
    }
}





function del_avatar_button() {
    del_div = document.getElementById("del_button");
    while (document.getElementById("del_button").childNodes.length > 0) {

        document.getElementById("del_button").removeChild(document.getElementById("del_button").childNodes[0]);
    }
}


function clearInputFile(f) {
    if (f.value) {
        try {
            f.value = ''; //for IE11, latest Chrome/Firefox/Opera...
        } catch (err) { }
        if (f.value) { //for IE5 ~ IE10
            var form = document.createElement('form'),
                parentNode = f.parentNode, ref = f.nextSibling;
            form.appendChild(f);
            form.reset();
            parentNode.insertBefore(f, ref);
        }
    }
}

let new_avatar_flag = false;

document.querySelector('#uploaded_avatar').addEventListener('change', function () {
    readURL();
    new_avatar_flag = true;
    del_avatar_button();
    create_del_button();
    
});


let uploadCrop;
var myImage = $('#myimg');

myImage.on('load', function() {
    if (new_avatar_flag) {   
        uploadCrop = $('#myimg').croppie({
            enableExif: true,
            viewport: {
                width: 300,
                height: 300,
                type: 'circle'
            },
            boundary: {
                width: 400,
                height: 400
            }
        });
        new_avatar_flag = false;
    }

});
