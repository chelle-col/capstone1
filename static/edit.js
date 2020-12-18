// Hold the filters applied to the canvas
let filters = [];

// Base URL
const base_url = 'http://127.0.0.1:5000/'

function drawPicture() {
    // Sets the canvas up
    const canvas = document.getElementById("canvas");
    const canvasContext = canvas.getContext("2d");
    const img = document.getElementById("image");
    canvasContext.drawImage(img, 0, 0);
}

//////// Filter Functions ////////////////////////////////////////////////

function filterToggle(filter){
    // Add/remove filter to filters
    if (filters.includes(filter)){
        const index = filters.indexOf(filter);
        filters.splice(index, 1);
    }else{
        filters.push(filter);
    }
}

function filterBackgroundToggle(id){
    $(`#${id}`).toggleClass('btn-primary');
    $(`#${id}`).toggleClass('btn-secondary');
}

function applyFilters(doRevert){
    // Applies all the filters stored in filters
    Caman('#canvas', function(){
        // TODO This introduces a race condtition. Need to fix. Doesn't break anything
        // Restores the orgional image between each update without showing
        if (doRevert){
            this.revert(false);
        }
        for (index in filters){
            switch (filters[index]){
                case 1:
                    this.vintage();
                    break;
                case 2:
                    this.lomo();
                    break;
                case 3:
                    this.clarity();
                    break;
                case 4:
                    this.sinCity();
                    break;
                case 5:
                    this.sunrise();
                    break;
                case 6:
                    this.crossProcess();
                    break;
                case 7:
                    this.orangePeel();
                    break;
                case 8:
                    
                    break;  
            }
        }
        this.render();
    });
}

function resetFilterButtons(){
    for(filter in filters){
        $(`#buttons`).find(`[data-id=${filters[filter]}]`).toggleClass('btn-secondary')
        $(`#buttons`).find(`[data-id=${filters[filter]}]`).toggleClass('btn-primary')
    }
}


//////////////////////////// Silder Functions //////////////////////////////

function handleSilderChange(doRevert){
    // Gets the values from the silders and sets them in the proper channels on the canvas
    sliderData = getSliderData();
    Caman('#canvas', function(){
        // Restores the orgional image between each update without drawing to page
        if (doRevert){
            this.revert(false);
        }
        this.saturation(sliderData.saturation).vibrance(sliderData.vibrance)
            .contrast(sliderData.contrast).exposure(sliderData.exposure)
            .hue(sliderData.hue).sepia(sliderData.sepia).render();
    });
    // Reapply filters to image
    applyFilters(false);
}

function handleSliderButton(evt){
    // Right and left buttons move the sliders up and down by one
    parent = evt.target.parentElement
    if(evt.target.dataset.direction === 'right'){
        parent.previousElementSibling.value = parseInt(parent.previousElementSibling.value) + 1;
    }else{
        parent.nextElementSibling.value = parent.nextElementSibling.value - 1;
    }
    handleSilderChange(true);
    applyFilters(false);
}

function resetSliders(){
    // Reset all sliders back to base
    $('#sliders').find('.slider').each((index, $slider)=>{
        num = $slider.getAttribute('value')
        $slider.value = num
    });
    handleSilderChange(false);
}

function resetFilters(){
    resetFilterButtons();
    filters.length = 0;
}

function getSliderData(){
    // Returns the values from the sliders
    return {
        'saturation' : parseInt($('#saturation').val()),
        'vibrance' : parseInt($('#vibrance').val()),
        'contrast' : parseInt($('#contrast').val()),
        'exposure' : parseInt($('#exposure').val()),
        'hue' : parseInt($('#hue').val()),
        'sepia' : parseInt($('#sepia').val())
    }
}

function setSliderData(sliderData){
    for (slider in sliderData){
        $(`#${slider}`).val(sliderData[slider])
    }
}
//////////////////// Handle Functions /////////////////////////////////

function handleButtonClick(evt){
    filterToggle(parseInt(evt.target.dataset.id));
    filterBackgroundToggle(evt.target.id);
    applyFilters(true);
    handleSilderChange(false);
}

function handleSideButtonClick(evt){
    if (evt.target.id === 'restore') {
        resetFilters();
        resetSliders();
        Caman('#canvas', function(){
            this.revert();
        });
    }else if (evt.target.id === 'save-filter'){
        $('#filter-name-form').show();
    }else if (evt.target.id === 'save-pic-filter'){
        $('picture-name-form').show();
    }
}

async function handleUserFilters(evt){
    resp = await axios.get(base_url + `/api/filter/${evt.target.value}`)
    setSliderData(resp.data.ranges);
    handleSilderChange(true);

    resetFilterButtons();
    filters = resp.data.presets;
    applyFilters(false);
    resetFilterButtons();
}

async function submitFilter(evt){
    evt.preventDefault();
   $('filter-name-form').hide();
    data = {
        'name' : $('#filter-name').val(),
        'ranges' : getSliderData(),
        'presets' : filters
    }
    resp = await axios.post(base_url + '/api/save_filter', {data: JSON.stringify(data)});
    // TODO do something with response???? Let user know filter was saved successfully/not
    console.log(resp.data)
}

async function submitImage(evt){
    $('picture-name-form').hide();
    evt.preventDefault();
}

/////////////////////////  Main /////////////////////////////////////

$(function() {
    // Main function
    drawPicture();
    $('#sliders').change( ()=>{
        handleSilderChange(true);
    }).on('click', 'button', (evt)=>{
        handleSliderButton(evt);
    })
    $('#buttons').on('click', 'button', (evt)=>{
        handleButtonClick(evt);
    })
    $('.side-buttons').on('click', (evt)=>{
        handleSideButtonClick(evt);
    })
    $('#filter-name-form').on('submit', (evt)=>{
        submitFilter(evt);
    })
    $('#picture-name-form').on('submit', (evt)=>{
        console.log('submitted')
    })
    $('#user-filters').change((evt)=>{
        handleUserFilters(evt);
    })
});