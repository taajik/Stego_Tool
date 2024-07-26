
let xmlhttp = new XMLHttpRequest();

function processProgress (oEvent) {
    document.getElementById('downloadlink').href = oEvent.target.responseText;
    document.getElementById('message').innerText = "Your file is ready!";
}

xmlhttp.addEventListener('progress', processProgress, false);
xmlhttp.open('get', process_path, true);
xmlhttp.send();
