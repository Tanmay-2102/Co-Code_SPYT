const dropArea = document.getElementById("drop-area")
const fileInput = document.getElementById("fileElem")
const preview = document.getElementById("preview-image")
const submitBtn = document.getElementById("submit-btn")
;["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults(e) {
  e.preventDefault()
  e.stopPropagation()
}
;["dragenter", "dragover"].forEach((eventName) => {
  dropArea.addEventListener(eventName, highlight, false)
})
;["dragleave", "drop"].forEach((eventName) => {
  dropArea.addEventListener(eventName, unhighlight, false)
})

function highlight() {
  dropArea.classList.add("highlight")
}

function unhighlight() {
  dropArea.classList.remove("highlight")
}

dropArea.addEventListener("drop", handleDrop, false)

function handleDrop(e) {
  const dt = e.dataTransfer
  const files = dt.files
  handleFiles(files)
}

fileInput.addEventListener("change", function () {
  handleFiles(this.files)
})

function handleFiles(files) {
  const file = files[0]
  if (file.type.startsWith("image/")) {
    const reader = new FileReader()
    reader.onload = (e) => {
      preview.src = e.target.result
      preview.style.display = "block"
      submitBtn.disabled = false
    }
    reader.readAsDataURL(file)
  }
}

submitBtn.addEventListener("click", () => {
  // In a real application, you would handle the file upload to a server here.
  // For this example, we'll just redirect to a new page with the image.
  const imageData = preview.src
  localStorage.setItem("uploadedImage", imageData)
  window.location.href = "output.html"
})

