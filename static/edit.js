// Hold the filters applied to the canvas
const filters = [];

function drawPicture() {
    // Sets the canvas up
    const canvas = document.getElementById("canvas");
    const canvasContext = canvas.getContext("2d");
    const img = document.getElementById("image");
    canvasContext.drawImage(img, 0, 0);
}

function filterToggle(filter){
    // Add/remove filter to filters
    if (filters.includes(filter)){
        const index = filters.indexOf(filter);
        filters.splice(index, 1);
    }else{
        filters.push(filter);
    }
}

function applyFilters(){
    // Applies all the filters stored in filters
    Caman('#canvas', function(){
        // Restores the orgional image between each update without showing
        // TODO This introduces a race condtition. Need to fix.
        this.revert(false);
        for (index in filters){
            switch (filters[index]){
                case 0:
                    this.vintage();
                    break;
                case 1:
                    this.lomo();
                    break;
                case 2:
                    this.clarity();
                    break;
                case 3:
                    this.sinCity();
                    break;
                case 4:
                    this.sunrise();
                    break;
                case 5:
                    this.crossProcess();
                    break;
                case 6:
                    this.orangePeel();
                    break;
                case 7:
                    
                    break;  
            }
        }
        this.render();
    });
}

function handleSilderChange(){
    // Gets the values from the silders and sets them in the proper channels on the canvas
    sliderData = getSliderData();
    Caman('#canvas', function(){
        // Restores the orgional image between each update without drawing to page
        this.revert(false);
        this.saturation(sliderData.saturation).vibrance(sliderData.vibrance)
            .contrast(sliderData.contrast).exposure(sliderData.exposure)
            .hue(sliderData.hue).sepia(sliderData.sepia).render();
    });
    // Reapply filters to image
    applyFilters();
}

function handleSliderButton(evt){
    // Right and left buttons move the sliders up and down by one
    parent = evt.target.parentElement
    if(evt.target.dataset.direction === 'right'){
        parent.previousElementSibling.value = parseInt(parent.previousElementSibling.value) + 1;
    }else{
        parent.nextElementSibling.value = parent.nextElementSibling.value - 1;
    }
    handleSilderChange();
    applyFilters();
}

function resetSliders(){
    // Reset all sliders back to base
    $('#sliders').find('.slider').each((index, $slider)=>{
        num = $slider.getAttribute('value')
        $slider.value = num
    });
    handleSilderChange();
}

function resetFilters(){
    // TODO
    filters.length = 0;
}

function handleButtonClick(evt){
    filterToggle(parseInt(evt.target.dataset.id));
    applyFilters();
}

function handleSideButtonClick(evt){
    if (evt.target.id === 'restore') {
        resetFilters();
        resetSliders();
        Caman('#canvas', function(){
            this.revert();
        });
    }
}

function getSliderData(){
    // Returns the values from the sliders
    return {
        'saturation' : parseInt($('#saturation').val()),
        'vibrance' : parseInt($('#vibrance').val()),
        'contrast' : parseInt($('#contrast').val()),
        'exposure' : parseInt($('#exposure').val()),
        'hue' : parseInt($('#hue').val()),
        'sepia' : parseInt($('#sepia').val())
    }
}

$(function() {
    // Main function
    drawPicture();
    $('#sliders').change( ()=>{
        handleSilderChange();
    }).on('click', 'button', (evt)=>{
        handleSliderButton(evt);
    })
    $('#buttons').on('click', (evt)=>{
        handleButtonClick(evt);
    })
    $('.side-buttons').on('click', (evt)=>{
        handleSideButtonClick(evt);
    })
});