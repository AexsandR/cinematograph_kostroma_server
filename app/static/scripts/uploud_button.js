let allFilesPreview = []; // Храним все выбранные файлы
let allFilesFrames = []; // Храним все выбранные файлы

function addFiles(newFiles, id) {
    // Добавляем новые файлы к существующим
    if (id == "fileListPreview"){
        allFilesPreview = [...allFilesPreview, ...newFiles];

    }else{
        if(allFilesFrames.length < 3){
            allFilesFrames = [...allFilesFrames, ...newFiles];
        }else{
            alert("можно только 3 кадра")
        }
    }

    updateFileList(id);
}

function updateFileList(id) {
    const fileListDiv = document.getElementById(id);
    fileListDiv.innerHTML = '';
    if (id == "fileListPreview"){
        allFiles = allFilesPreview;

    }else{

        allFiles = allFilesFrames;
    }

    allFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
        ${file.name}
        <button onclick="removeFile(${index}, '${id}')">×</button>
      `;
        fileListDiv.appendChild(fileItem);
    });
}

function removeFile(index, id) {
    if (id == "fileListPreview"){
        allFilesPreview.splice(index, 1);

    }else{
        allFilesFrames.splice(index, 1);
    }
    updateFileList(id);
}