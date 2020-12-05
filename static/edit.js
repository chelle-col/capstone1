function drawPicture() {
    const canvas = document.getElementById("canvas");
    const canvasContext = canvas.getContext("2d");
    const img = document.getElementById("image");
    canvasContext.drawImage(img, 0, 0);
}

function handleSilderChange(evt){
    sliderData = getSliderData();
    console.log(sliderData)
    Caman('#canvas', $('#image'), function(){
        this.revert(false);
        this.saturation(sliderData.saturation).vibrance(sliderData.vibrance)
            .contrast(sliderData.contrast).exposure(sliderData.exposure)
            .hue(sliderData.hue).sepia(sliderData.sepia).render();
    })
}

function getSliderData(){
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
    drawPicture();
    Caman('#canvas', function () {
        console.log(this)
        this.brightness(5);
        this.render();
    });
    $('#sliders').change( (evt)=>{
        console.log(evt.target)
        handleSilderChange(evt);
    })
});