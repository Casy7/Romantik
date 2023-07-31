
function show_password() {
    pwd_field = document.getElementById("password_field")
    if (pwd_field.type == 'password') {
        pwd_field.type = "text";
    }
    else {
        pwd_field.type = "password";
    }
}