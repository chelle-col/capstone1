const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function displayImage(){
    let file = document.querySelector('#upload-file').files[0];
    let reader = new FileReader();
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
                    height:330
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
            'id' : $('#navbarDropdown').data('userid'),
            'image': canvas.toDataURL(),
            'width': canvas.width,
            'height': canvas.height
        }
        resp = await axios.post( base_url + '/api/image/upload', {data: JSON.stringify(data)})
        window.location.href = base_url + `/image/${resp.data}/new`
    })
});