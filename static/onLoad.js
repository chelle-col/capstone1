async function updateFilter(evt, id){
    evt.preventDefault()
    sliderData = getSliderData()
    data = {
        'id' : $('#navbarDropdown').data('userid'),
        'filter_id' : id,
        'ranges' : sliderData
    }
    resp = await axios.post(base_url + '/api/update_filter', {'data': JSON.stringify(data)})
}

$(function(){
    handleUserFilters($('#edit-filter-form').data('id'))
    $('#save-filter').on('click', ()=>{
        $('#edit-filter-form').toggleClass('hide')
    })
    $('#edit-filter-form').on('submit', (evt)=>{
        updateFilter(evt, $('#edit-filter-form').data('id'));
    })
})