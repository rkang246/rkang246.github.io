import imageFiles from './image_list.js';

function populatePhotoGrid() {
    const container = document.querySelector(".container3");
    const photoGrid = document.getElementById("photo-grid");

    photoGrid.innerHTML = 'HELLO';
}

document.addEventListener('DOMContentLoaded', populatePhotoGrid);