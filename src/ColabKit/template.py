AUDIO_SHOW = """<audio controls src="%s"></audio>"""

VIDEO_SHOW = """<video controls width=500><source src="%s" type="video/mp4"></video>"""

AUDIO_RECORD = """
<script>
    var my_div = document.createElement("DIV");
    var recordButton = document.createElement("BUTTON");

    my_div.style.display = "flex";
    my_div.style.flexDirection = "column";
    my_div.style.gap = "10px";
    my_div.style.alignItems = "center";
    my_div.style.padding = "10px";

    recordButton.style.backgroundColor = "red";
    recordButton.style.color = "white";
    recordButton.style.margin = "0 auto";
    recordButton.style.border = "none";
    recordButton.style.borderRadius = "5px";
    recordButton.style.padding = "5px 10px";
    recordButton.style.cursor = "pointer";

    my_div.appendChild(recordButton);
    document.body.appendChild(my_div);

    var base64data = 0;
    var reader;
    var recorder, gumStream;

    var handleSuccess = function (stream) {
      gumStream = stream;
      var options = {
        mimeType: 'audio/webm;codecs=opus'
      };
      recorder = new MediaRecorder(stream);
      recorder.ondataavailable = function (e) {
        var url = URL.createObjectURL(e.data);
        var preview = document.createElement('audio');
        preview.controls = true;
        preview.src = url;
        my_div.appendChild(preview);

        reader = new FileReader();
        reader.readAsDataURL(e.data);
        reader.onloadend = function () {
          base64data = reader.result;
        }
      };
      recorder.start();
    };

    recordButton.innerText = "Recording... press to stop";

    navigator.mediaDevices.getUserMedia({ audio: true }).then(handleSuccess);


    function toggleRecording() {
      if (recorder && recorder.state == "recording") {
        recordButton.innerText = "Saving the recording... please wait!"
        recordButton.style.backgroundColor = "yellow";
        recordButton.style.color = "black";
        recorder.stop();
        gumStream.getAudioTracks()[0].stop();
      }
    }

    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    var data = new Promise(resolve => {
      recordButton.onclick = () => {
        toggleRecording()

        sleep(2000).then(() => {
          resolve(base64data.toString())
        });
      }
    });

  </script>
"""

SAVED_AUDIO_RECORDING = """
<script>
recordButton.innerText = "Audio successfully saved"
recordButton.style.backgroundColor = "green";
recordButton.style.color = "white";
</script>
"""
