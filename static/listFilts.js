async function remove_filter(element, id){
    // axios to /api/remove_filter
    resp = await axios.post('http://127.0.0.1:5000/api/remove_filter', {'data': JSON.stringify(id)})
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
        $('#alert-modal').find('.modal-body').text(`Any image/filter information associated with filter ${evt.target.parentElement.parentElement.previousElementSibling.innerText} will be deleted. Contiue?`);
        $('#alert-modal').modal(focus=true)
  
        $('.modal-button').on('click', ()=>{
            remove_filter(evt.target.parentElement.parentElement.parentElement, id);
        })
    })
});