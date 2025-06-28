function addFiles(files, id, fileid) {
    const fileListDiv = document.getElementById(id);
    fileListDiv.innerHTML = '';

    if (!files || files.length === 0) {
        console.log("Файл не выбран");
        return;
    }

    const file = files[0]; // Берём только первый файл
    console.log(file);

    const fileItem = document.createElement('div');

    fileItem.innerHTML = `
            <span>${file.name}</span>
            <button type="button" onclick="cancellation('${fileid}', '${id}')">×</button>
        `;
    fileListDiv.appendChild(fileItem);
}

function cancellation(input_id, id){
    const fileListDiv = document.getElementById(id);
    fileListDiv.innerHTML = '';
    const fileInput = document.getElementById(input_id);
    fileInput.value = '';
}