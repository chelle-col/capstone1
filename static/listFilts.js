async function remove_filter(element, id){
    // axios to /api/remove_filter
    data = {
        'id' : $('#navbarDropdown').data('userID'),
        'filter_id' : id
    }
    resp = await axios.post('https://mycapstone1.herokuapp.com/api/remove_filter', {'data': JSON.stringify(data)})
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
        $('#alert-modal').find('.modal-body').text(`Any image information associated with filter ${evt.target.parentElement.parentElement.previousElementSibling.innerText} will be deleted. Contiue?`);
        $('#alert-modal').modal(focus=true)
  
        $('.modal-button').on('click', ()=>{
            remove_filter(evt.target.parentElement.parentElement.parentElement, id);
        })
    })
});