
var arrow_icon = document.getElementById('arrow_icon');
var password_field = document.getElementById('password_field');

document.getElementById('cipher_option').addEventListener('click', function() {
    arrow_icon.classList.toggle('arrow_up');
    arrow_icon.classList.toggle('arrow_down');

    if (password_field.style.display === 'block') {
        password_field.style.display = 'none';
        document.getElementById('id_password').value = '';
    } else {
        password_field.style.display = 'block';
    }
});
