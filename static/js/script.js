function startWebcam() {
  let emotionDetectorDiv = document.getElementById('emotion-detector');
  let videoContainerDiv = emotionDetectorDiv.querySelector('.video-container');
  let imgElement = document.createElement('img');
  imgElement.classList.add('outer-shadow');
  imgElement.setAttribute('id', 'bg');
  imgElement.setAttribute('class', 'center img-fluid');
  imgElement.setAttribute('src', "/video_feed");
  videoContainerDiv.appendChild(imgElement);

  emotionDetectorDiv.style.display = 'block';

  setTimeout(function() {
    emotionDetectorDiv.style.display = 'none';
    videoContainerDiv.removeChild(imgElement);

    // fetch('/get_emotion').then(function(response) {
    //   return response.text();
    // }).then(function(emotion) {
    //   console.log(emotion);
    //   // document.getElementById('emotion-input').value = emotion;
    //   // document.getElementById('emotion-form').submit();
    // });
  }, 5500);
}
