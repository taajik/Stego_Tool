
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
    payload_file_input.value = '';
    payload_label.htmlFor = 'id_payload_text';
});

document.getElementById('payload_file_label').addEventListener('click', function() {
    payload_file_field.style.display = 'block';
    payload_file_input.required = true;
    payload_text_field.style.display = 'none';
    payload_text_input.required = false;
    payload_text_input.value = '';
    payload_label.htmlFor = 'id_payload_file';
});
