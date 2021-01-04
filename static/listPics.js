async function remove_filter(element, id){
    // axios to /api/remove_filter
    data = {
        'id' : $('#navbarDropdown').data('userid'),
        "filter_id" : id
    }
    console.log(data)
    // resp = await axios.post('https://mycapstone1.herokuapp.com/api/remove_picture', {'data': JSON.stringify(data)})
    resp = await axios.post('http://127.0.0.1:5000//api/remove_picture', {'data': JSON.stringify(data)})
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