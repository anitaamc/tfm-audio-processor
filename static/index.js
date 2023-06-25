let mediaRecorder;
let recordedChunks = [];

function startRecording() {
    if (!navigator.mediaDevices.getUserMedia) {
        document.getElementById("message").innerHTML = "La grabación de audio no es compatible en este navegador.";
        return;
    }

    var constraints = { audio: true };
    var chunks = [];

    navigator.mediaDevices.getUserMedia(constraints)
        .then(function(stream) {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(event) {
                chunks.push(event.data);
            };

            mediaRecorder.onstop = function() {
                const audioBlob = new Blob(chunks, { type: 'audio/wav' });

                const formData = new FormData();
                formData.append('audio', audioBlob, 'audio.wav');

                fetch('/save_audio', {
                    method: 'POST',
                    body: formData
                })
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    var message = data.message;
                    document.getElementById("message").innerHTML = message;
                });
            };

            mediaRecorder.start();
            document.getElementById("message").innerHTML = "Grabando...";
        })
        .catch(function(error) {
            console.log("Ocurrió un error al acceder al dispositivo de audio: " + error);
            document.getElementById("message").innerHTML = "Error al acceder al dispositivo de audio.";
        });
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById("message").innerHTML = "Grabación parada";

    const audioBlob = new Blob(recordedChunks, { type: 'audio/wav' });

    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');

    fetch('/save_audio', {
        method: 'POST',
        body: formData
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        var message = data.message;
        document.getElementById("message").innerHTML = message;
    });
}

function overwriteKeywords() {
    var keywords = document.getElementById("keywords").value.split(",");
    fetch('/overwrite_keywords', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ keywords: keywords })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        var message = data.message;
        document.getElementById("message").innerHTML = message;
    });
}
