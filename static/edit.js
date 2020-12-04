function drawPicture() {
    const canvas = document.getElementById("canvas");
    const canvasContext = canvas.getContext("2d");
    const img = document.getElementById("image-id");
    canvasContext.drawImage(img, 0, 0);
}

$(function() {
    console.log( "ready!" );
    drawPicture();
    Caman('#canvas', function () {
        this.brightness(20);
        this.contrast(40);
        this.render();
    });
});