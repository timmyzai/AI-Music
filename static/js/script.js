const recSongsList = document.querySelector('#rec-songs-list');
const loadingIndicatorDiv = document.getElementById('loading-indicator');
const emotionDetectorDiv = document.getElementById('emotion-detector');
const videoContainerDiv = emotionDetectorDiv.querySelector('.video-container');
const emotionInput = document.getElementById('emotion-input')
const webcamEmotionForm = document.getElementById('webcam-emotion-form');

function startWebcam() {
  if (recSongsList) {
    recSongsList.innerHTML = '';
  }
  loadingIndicatorDiv.style.display = 'block';

  let imgElement = document.createElement('img');
  imgElement.classList.add('outer-shadow');
  imgElement.setAttribute('id', 'bg');
  imgElement.setAttribute('class', 'center img-fluid');
  imgElement.setAttribute('src', "/video_feed");
  videoContainerDiv.appendChild(imgElement);

  emotionDetectorDiv.style.display = 'block';

  setTimeout(function () {
    emotionDetectorDiv.style.display = 'none';
    loadingIndicatorDiv.style.display = 'none';
    videoContainerDiv.removeChild(imgElement);

    fetch('/get_emotion').then(function (response) {
      return response.text();
    }).then(function (emotion) {
      emotionInput.value = emotion;
      webcamEmotionForm.submit();
    });
  }, 5000);
}
