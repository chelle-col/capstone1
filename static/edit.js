function drawPicture() {
    // Sets the canvas up
    const canvas = document.getElementById("canvas");
    const canvasContext = canvas.getContext("2d");
    const img = document.getElementById("image");
    canvasContext.drawImage(img, 0, 0);
}

function camanSwitch(num){
    switch (num){
        case 0:
            Caman('#canvas', function(){
                this.vintage().render();
            })
            break;
        case 1:
            Caman('#canvas', function(){
                this.lomo().render();
            })
            break;
        case 2:
            Caman('#canvas', function(){
                this.clarity().render();
            })
            break;
        case 3:
            Caman('#canvas', function(){
                this.sinCity().render();
            })
            break;
        case 4:
            Caman('#canvas', function(){
                this.sunrise().render();
            })
            break;
        case 5:
            Caman('#canvas', function(){
                this.crossProcess().render()
            })
            break;
        case 6:
            Caman('#canvas', function(){
                this.orangePeel().render();
            })
            break;
        case 7:
            Caman('#canvas', function(){
                
            })
            break;  
    }
}

function handleSilderChange(){
    // Gets the values from the silders and sets them in the proper channels on the canvas
    sliderData = getSliderData();
    Caman('#canvas', function(){
        // Restores the orgional image between each update
        this.revert(false);
        this.saturation(sliderData.saturation).vibrance(sliderData.vibrance)
            .contrast(sliderData.contrast).exposure(sliderData.exposure)
            .hue(sliderData.hue).sepia(sliderData.sepia).render();
    })
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
}

function resetSliders(){
    console.log($('#sliders').children)
}

function handleButtonClick(evt){
    camanSwitch(parseInt(evt.target.dataset.id));
}

function handleSideButtonClick(evt){
    if (evt.target.id === 'restore') {
        Caman('#canvas', function(){
            this.revert();
        });
        resetSliders();
    }
}

function getSliderData(){
    // Returns the values from the sliders
    return {
        'saturation' : $('#saturation').val(),
        'vibrance' : $('#vibrance').val(),
        'contrast' : $('#contrast').val(),
        'exposure' : $('#exposure').val(),
        'hue' : $('#hue').val(),
        'sepia' : $('#sepia').val()
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