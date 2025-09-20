document.addEventListener('DOMContentLoaded', function () {
    const selectImageButton = document.getElementById('select-images-button');
    const actualField = document.getElementById('image-upload');
    const imagePreview = document.getElementById('image-preview');
    const twinButtons = document.getElementById('twin-buttons');
    const maxFiles = 10;
    let selectedFiles = [];

    selectImageButton.onclick = function() {
        actualField.click();
    };

    actualField.addEventListener('change', async function(event) {
        const files = Array.from(event.target.files);

        if (files.length + selectedFiles.length > maxFiles) {
            alert(`You can only select up to ${maxFiles} images`);
            return;
        }

        const convertedFiles = await convertAndStoreFiles(files);
        selectedFiles = [...selectedFiles, ...convertedFiles];
        updatePreview();
    });

    function convertAndStoreFiles(files) {
        const conversionPromises = files.map(async (file, index) => {
            if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
                try {
                    //add loader
                    const loader = document.createElement('div');
                    loader.classList.add('loader');
                    loader.textContent = 'loading...';
                    imagePreview.appendChild(loader);

                    const convertedBlob = await heic2any({
                        blob: file,
                        toType: 'image/jpeg',
                    });

                    file = new File([convertedBlob], `${file.name.split('.')[0]}.jpg`, { type: 'image/jpeg' });
                    //remove loader
                    imagePreview.removeChild(loader);
                } catch (error) {
                    console.error('Error converting HEIC file:', error);
                }
            }
            const fileIndex = selectedFiles.length + index;
            const fileInput = document.getElementById(`id_image${fileIndex + 1}`);
            if (fileInput) {
                const dt = new DataTransfer();
                dt.items.add(file);
                fileInput.files = dt.files;
            }
            return file;
        });

        return Promise.all(conversionPromises);
    }

    function updatePreview() {
        imagePreview.innerHTML = '';  // Clear existing previews
        selectedFiles.forEach((file, index) => createImagePreview(file, index));
    }

    function createImagePreview(file, index) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgContainer = document.createElement('div');
            imgContainer.classList.add('img-container');

            const img = document.createElement('img');
            img.src = e.target.result;

            const label = document.createElement('div');
            label.textContent = `image ${index + 1}`;
            label.style.bottom = '0';
            label.style.position = 'absolute';
            label.style.backgroundColor = 'white';
            label.style.borderRadius = '5px';
            label.style.zIndex = '1000';

            const removeButton = document.createElement('button');
            removeButton.textContent = 'X';
            removeButton.onclick = function() {
                // Clear the file input and remove the image
                const fileInput = document.getElementById(`id_image${index + 1}`);
                if (fileInput) fileInput.value = '';
                selectedFiles.splice(index, 1);
                updatePreview();
            };

            const changeButton = document.createElement('button');
            changeButton.type='button';
            changeButton.textContent = 'change';
            changeButton.style.position = 'absolute';
            changeButton.style.width = 'fit-content';
            changeButton.style.height = 'fit-content';
            changeButton.style.left = '-55px';
            changeButton.style.top = '0';
            changeButton.style.borderRadius = '5px';
            changeButton.style.fontSize = '12px';
            changeButton.style.padding = '0';
            changeButton.onclick = function() {
                const changeInput = document.createElement('input');
                changeInput.type = 'file';
                changeInput.accept = 'image/*';
                changeInput.style.display = 'none';

                const fileInput = document.getElementById(`id_image${index + 1}`);
                if (fileInput) fileInput.value = '';

                changeInput.onchange = async function(event) {
                    const newFile = event.target.files[0];
                    if (newFile) {
                        if (newFile.type !== 'image/jpeg' && newFile.type !== 'image/png') {
                            try {
                                const convertedBlob = await heic2any({
                                    blob: newFile,
                                    toType: 'image/jpeg',
                                });

                                selectedFiles[index] = new File([convertedBlob], `${newFile.name.split('.')[0]}.jpg`, { type: 'image/jpeg' });
                            } catch (error) {
                                console.error('Error converting HEIC file:', error);
                                return;
                            }
                        } else {
                            selectedFiles[index] = newFile;
                        }

                        const fileInput = document.getElementById(`id_image${index + 1}`);
                        if (fileInput) {
                            const dt = new DataTransfer();
                            dt.items.add(selectedFiles[index]);
                            fileInput.files = dt.files;
                        }

                        // Update the preview for the changed image
                        updatePreview();
                    }
                };

                document.body.appendChild(changeInput);
                changeInput.click();
                document.body.removeChild(changeInput);
            };

            imgContainer.appendChild(label);
            imgContainer.appendChild(img);
            imgContainer.appendChild(removeButton);
            imgContainer.appendChild(changeButton);
            imagePreview.appendChild(imgContainer);
        };

        reader.readAsDataURL(file);
    }

    // Add button to handle adding new images
    const addButton = document.createElement('button');
    addButton.type='button';
    addButton.style.position='relative';
    addButton.textContent = '+';
    addButton.style.borderRadius='50%';
    addButton.style.width='22px';
    addButton.style.height='22px';
    addButton.style.marginLeft='-150px';
    addButton.style.marginTop='0';
    addButton.style.paddingBottom='10px';
    addButton.style.backgroundColor='black';
    
    
    addButton.onclick = function() {
        if (selectedFiles.length >= maxFiles) {
            alert(`You can only have up to ${maxFiles} images`);
            return;
        }
        actualField.click();
    };
    twinButtons.appendChild(addButton);
});