
let xhr = new XMLHttpRequest();
xhr.responseType = 'json';

function processFinished (e) {
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {

            let result = e.target.response['result']
            document.getElementById('message').innerText = 'Your result is ready!';
            if (result[1]) {
                document.getElementById('text-payload').innerText = result[0];
            } else {
                document.getElementById('downloadlink').href = result[0];
                document.getElementById('downloadlink').innerText = 'Download'
            }

        } else {
            document.getElementById('message').innerText = 'There was an error!';
        }
    }
}

xhr.addEventListener('readystatechange', processFinished, false);
xhr.open('get', process_path, true);
xhr.send();
