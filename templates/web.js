document.addEventListener('DOMContentLoaded', function () {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('audio-file');
    const browseButton = document.getElementById('browse-button');

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('Default behavior prevented');
    }

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            console.log(`${eventName} event triggered`);
            dropArea.classList.add('highlight');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            console.log(`${eventName} event triggered`);
            dropArea.classList.remove('highlight');
        });
    });

    dropArea.addEventListener('drop', (e) => {
        console.log('File dropped');
        let dt = e.dataTransfer;
        let files = dt.files;
        fileInput.files = files;
        dropArea.querySelector('p').textContent = files[0].name;
    });

    browseButton.addEventListener('click', () => {
        console.log('Browse button clicked');
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        const fileName = fileInput.files[0]?.name || "No file selected";
        dropArea.querySelector('p').textContent = fileName;
        console.log(`File selected: ${fileName}`);
    });
});
