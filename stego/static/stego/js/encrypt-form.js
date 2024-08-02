
var payload_text_field = document.getElementById('payload_text_field');
var payload_file_field = document.getElementById('payload_file_field');
var payload_text_input = document.getElementById('id_payload_text');
var payload_file_input = document.getElementById('id_payload_file');
var payload_label = document.getElementById('payload_label');

document.getElementById('payload_text_label').addEventListener('click', function() {
    payload_text_field.style.display = 'block';
    payload_text_input.required = true;
    payload_file_field.style.display = 'none';
    payload_file_input.required = false;
    payload_label.htmlFor = 'id_payload_text';
});

document.getElementById('payload_file_label').addEventListener('click', function() {
    payload_file_field.style.display = 'block';
    payload_file_input.required = true;
    payload_text_field.style.display = 'none';
    payload_text_input.required = false;
    payload_label.htmlFor = 'id_payload_file';
});


var arrow_icon = document.getElementById('arrow_icon');
var password_field = document.getElementById('password_field');

document.getElementById('encipher').addEventListener('click', function() {
    arrow_icon.classList.toggle('arrow_up');
    arrow_icon.classList.toggle('arrow_down');

    if (password_field.style.display === 'block') {
        password_field.style.display = 'none';
        document.getElementById('id_password').value = '';
    } else {
        password_field.style.display = 'block';
    }
});
