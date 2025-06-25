document.getElementById('uploadForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const fileInput = document.getElementById('fileInput');
  const languageSelect = document.getElementById('languageSelect');
  const statusDiv = document.getElementById('status');
  const progressWrapper = document.getElementById('progressWrapper');
  const progressBar = document.getElementById('progressBar');
  const waitMessage = document.getElementById('waitMessage');

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('language', languageSelect.value);

  statusDiv.innerHTML = '<p>Procesando tu vídeo...</p>';
  progressWrapper.style.display = 'block';
  progressBar.value = 0;

  let progress = 0;
  const duration = 180000;
  const intervalTime = 1000;
  const increment = 90 / (duration / intervalTime);
  const interval = setInterval(() => {
    progress += increment;
    progressBar.value = progress;
    if (progress >= 90) {
      progressBar.value = 90;
      clearInterval(interval);
      waitMessage.innerHTML = 'Esperando a que se complete la transcripción...';
    }
  }, intervalTime);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    const disposition = response.headers.get('Content-Disposition');
    const filename = disposition ? disposition.split('filename=')[1].replace(/"/g, '') : 'transcription.zip';
    return response.blob().then(blob => ({ blob, filename }));
  })
  .then(({ blob, filename }) => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();

    statusDiv.innerHTML = '<p>La transcripción está lista para descargar.</p>';
    progressWrapper.style.display = 'none';

    setTimeout(() => {
      window.location.reload();
    }, 1000);
  })
  .catch(error => {
    console.error('Error:', error);
    statusDiv.innerHTML = '<p style="color: red;">Hubo un error al procesar el archivo. Inténtalo de nuevo.</p>';
    progressWrapper.style.display = 'none';
  });
});

