
var arrow_icon = document.getElementById('arrow_icon');
var password_field = document.getElementById('password_field');
var password_input = document.getElementById('id_password');

document.getElementById('cipher_option').addEventListener('click', function() {
    arrow_icon.classList.toggle('arrow_up');
    arrow_icon.classList.toggle('arrow_down');

    if (password_field.style.display === 'block') {
        password_field.style.display = 'none';
        password_input.value = '';
    } else {
        password_field.style.display = 'block';
    }
});


var showhide_btn = document.getElementById('showhide_btn');

function showHidePW() {
    if (password_input.type === 'password') {
        password_input.type = 'text';
    } else {
        password_input.type = 'password';
    }

    if (showhide_btn.innerText === 'show') {
        showhide_btn.innerText = 'hide';
    } else {
        showhide_btn.innerText = 'show';
    }
}
