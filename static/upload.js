const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function displayImage(){
    var file = document.querySelector('#upload-file').files[0];
    var reader = new FileReader();
    if (file) {
        fileName = file.name;
        reader.readAsDataURL(file);
    }
    reader.addEventListener("load", function () {
        img = new Image();
        img.src = reader.result;
        img.onload = function () {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0, img.width, img.height);
            Caman('#canvas', function () {
                this.resize({
                    height:500
                }).render();
            })
        }
    });
}

$(function() {
    $("#upload-file").on("change", ()=>{
        displayImage();
    });

    $('#upload').on('click', async ()=>{
        data = {
            'image': canvas.toDataURL(),
            'width': canvas.width,
            'height': canvas.height
        }
        resp = await axios.post('https://mycapstone1.herokuapp.com/api/upload_picture', {data: JSON.stringify(data)})
        window.location.href = `https://mycapstone1.herokuapp.com/my_image/${resp.data}/edit`
    })
});