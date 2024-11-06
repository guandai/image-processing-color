async function processImage() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');
    if (!fileInput.files.length) {
        status.textContent = "Please select a file first!";
        return;
    }

    status.textContent = "Processing...";

    // Prepare the file for upload
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/process-image', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            // Create a download link and automatically click it to download
            const blob = await response.blob();
            const downloadUrl = URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = downloadUrl;
            downloadLink.download = 'processed_image.jpg';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            status.textContent = "Download complete!";
        } else {
            status.textContent = "Error processing the image.";
        }
    } catch (error) {
        status.textContent = "Error: " + error.message;
    }
}
