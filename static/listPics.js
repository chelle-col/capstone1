async function remove_filter(element, id){
    // axios to /api/image/<id>/delete
    data = {
        'user_id' : $('#navbarDropdown').data('userid'),
        "image_id" : id
    }
    console.log(data)
    resp = await axios.post( base_url + `/api/image/${id}/delete`, {'data': JSON.stringify(data)})
    
    // remove from dom
    element.remove();
}

$(function(){

    // select class remove
    $('.remove').on('click', async (evt)=>{
        evt.preventDefault()
        // get id of filter
        id = evt.target.parentElement.parentElement.dataset.id

        // popup to confirm removal
        $('#alert-modal').find('.modal-title').text('Irreversable Changes');
        $('#alert-modal').find('.modal-body').text(`The picture ${evt.target.parentElement.parentElement.previousElementSibling.innerText} will be deleted. This action is irreversable. Contiue?`);
        $('#alert-modal').modal(focus=true)
  
        $('.modal-button').on('click', ()=>{
            remove_filter(evt.target.parentElement.parentElement.parentElement, id);
        })
    })
});