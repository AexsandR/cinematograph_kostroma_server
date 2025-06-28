function addFiles(files, id) {
    const fileListDiv = document.getElementById(id);
    fileListDiv.innerHTML = '';

    if (!files || files.length === 0) {
        console.log("Файл не выбран");
        return;
    }

    const file = files[0]; // Берём только первый файл
    console.log(file);

    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.textContent = file.name;
    fileListDiv.appendChild(fileItem);
}