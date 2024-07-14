let dropZone = document.getElementById("dropZone");
let fileInput = document.getElementById("fileInput");
let fileName = document.getElementById("fileName");
let uploadForm = document.getElementById("uploadForm");
let generateBtn = document.getElementById("generateBtn");

const preprocessingRadios = document.querySelectorAll('input[name="preprocessing"]');
const processingTextRank = document.getElementById('processing-textrank');
const processingLSA = document.getElementById('processing-lsa');
const processingFalcon = document.getElementById('processing-falcon')

// Disable radio options in certain cases. 
function updateProcessingOptions() {
    const selectedPreprocessing = document.querySelector('input[name="preprocessing"]:checked').value;
    const selectedProcessing = document.querySelector('input[name="processing"]:checked').value;

    if (selectedPreprocessing === 'textrank' || selectedPreprocessing === 'lsa') {

        // If currently choosing the 2 below, force choose falcon
        if(selectedProcessing === 'textrank' || selectedProcessing === 'lsa'){
            processingFalcon.checked = true;
        }
        
        processingTextRank.disabled = true;
        processingLSA.disabled = true;      
    } else {
        processingTextRank.disabled = false;
        processingLSA.disabled = false;
    }
}

preprocessingRadios.forEach(radio => {
    radio.addEventListener('change', updateProcessingOptions);
});

// Call the function initially to set the correct state
updateProcessingOptions();

dropZone.addEventListener("click", function () {
    fileInput.click();
});

fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
        fileName.textContent = "File: " + fileInput.files[0].name;
    } else {
        fileName.textContent = "";
    }
});

dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.add("dragover");
});

dropZone.addEventListener("dragleave", function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove("dragover");
});

dropZone.addEventListener("drop", function (e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove("dragover");

    let file = e.dataTransfer.files[0];
    fileInput.files = e.dataTransfer.files;
    fileName.textContent = "File: " + file.name;
});

generateBtn.addEventListener("click", function () {
    if (!fileInput.files.length) {
        alert("Please select a file before submitting.");
        return;
    }

    // Create a new FormData object
    let formData = new FormData(uploadForm);
    formData.append('preprocessing', document.querySelector('input[name="preprocessing"]:checked').value);
    formData.append('processing', document.querySelector('input[name="processing"]:checked').value);

    fetch(uploadForm.action, {
        method: "POST",
        body: formData,
    })
    .then(response => response.text().then(text => {
        if (!response.ok) {
            throw new Error(text);
        }
        return text;
    }))
    .then(data => {
        document.getElementById("result-section").style.display = "block";
        document.getElementById("result-section").innerHTML = data;
        document.getElementById("error-section").style.display = "none";
    })
    .catch(error => {
        document.getElementById("error-section").style.display = "block";
        document.getElementById("error-section").innerHTML = error.message;
        document.getElementById("result-section").style.display = "none";
    });
});