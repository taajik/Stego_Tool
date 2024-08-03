
var message = document.getElementById('message');
var text_payload = document.getElementById('text-payload');
var download_link = document.getElementById('download-link');


var copy_button = document.getElementById('copy-button');
copy_button.addEventListener('click', function() {
    text_payload.select();
    document.execCommand('copy');
    copy_button.innerText = 'Copied!';
});


let xhr = new XMLHttpRequest();
xhr.responseType = 'json';

function processFinished (e) {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {

            let result = e.target.response['result'];
            message.innerText = 'Your result is ready!';
            if (result[1]) {
                text_payload.innerText = result[0];
                document.getElementById('text-box').style.display = 'flex';
            } else {
                download_link.href = result[0];
                download_link.style.display = 'inline';
            }

        } else {
            message.innerText = 'There was an error!';
        }
    }
}

xhr.addEventListener('readystatechange', processFinished, false);
xhr.open('get', process_path, true);
xhr.send();
