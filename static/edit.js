// Hold the filters applied to the canvas
let filters = [];

// Base URL
const base_url = 'http://mycapstone1.herokuapp.com'
// const base_url = 'http://127.0.0.1:5000'

function drawPicture() {
    // Sets the canvas up
    const canvas = document.getElementById("canvas");
    const canvasContext = canvas.getContext("2d");
    const img = document.getElementById("image");
    canvasContext.drawImage(img, 0, 0);
    Caman('#canvas', function(){
        this.resize({
            width: 400
        }).render();
    })
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
    // Uses the id of an element to toggle between primary and secondary
    $(`#${id}`).toggleClass('btn-primary');
    $(`#${id}`).toggleClass('btn-secondary');
}

function applyFilters(doRevert){
    // Applies all the filters stored in filters
    Caman('#canvas', function(){
        // This introduces a race condtition. Need to fix at a later date. Doesn't break anything
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
                    this.love();
                    break;
                case 9:
                    this.grungy();
                    break;
                case 10:
                    this.jarques();
                    break;  
                case 11:
                    this.pinhole();
                    break;
                case 12:
                    this.oldBoot();
                    break;
                case 13:
                    this.glowingSun();
                    break;  
                case 14:
                    this.hazyDays();
                    break;  
                case 15:
                    this.herMajesty();
                    break;  
                case 16:
                    this.nostalgia();
                    break;  
                case 17:
                    this.hemingway();
                    break;  
                case 18:
                    this.concentrate();
                    break;                                                                
            }
        }
        this.render();
    });
}

function resetFilterButtons(){
    // Useing the filters to turn off primary background
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
            .hue(sliderData.hue).sepia(sliderData.sepia).noise(sliderData.noise).render();
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
    // Sets the filter, buttons and array
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
        'sepia' : parseInt($('#sepia').val()),
        'noise' : parseInt($('#noise').val())
    }
}

function setSliderData(sliderData){
    // Sets the slider data to the enw slider data
    for (slider in sliderData){
        $(`#${slider}`).val(sliderData[slider])
    }
}
//////////////////// Handle Functions /////////////////////////////////

function handleButtonClick(evt){
    // Handles when the user presses one of the filter buttons
    filterToggle(parseInt(evt.target.dataset.id));
    filterBackgroundToggle(evt.target.id);
    applyFilters(true);
    handleSilderChange(false);
}

function handleSideButtonClick(evt){
    // Handles when the user pushes one of the side buttons, restore/save filter/save filter and pic
    if (evt.target.id === 'restore') {
        resetFilters();
        resetSliders();
        Caman('#canvas', function(){
            this.revert();
        });
    }else if (evt.target.id === 'save-filter'){
        $('#filter-name-form').toggleClass('hide');
    }else if (evt.target.id === 'save-pic-filter'){
        $('#picture-name-form').toggleClass('hide');
    }
}

async function handleUserFilters(id){
    // Gets the filters from the database that the user has saved and applies them to the image
    resp = await axios.get(base_url + `/api/filter/${id}`)
    // Use the slider data from the database
    setSliderData(resp.data.ranges);
    handleSilderChange(true);
    // Set the filter buttons all to base
    resetFilterButtons();
    filters = resp.data.presets;
    applyFilters(false);
    // Toggle the buttons to show which are active
    resetFilterButtons();
}

async function submitFilter(evt){
    // Sends the filter information to the database to be saved
    evt.preventDefault();
    // Hide the form on submit
   $('#filter-name-form').toggleClass('hide');
    data = {
        'id' : $('#navbarDropdown').data('userid'),
        'name' : $('#filter-name').val(),
        'ranges' : getSliderData(),
        'presets' : filters
    }
    resp = await axios.post(base_url + '/api/filter/new', {data: JSON.stringify(data)});
    // Feedback to show the user their filter was saved
    showSavedData(data['name']);
}

function showSavedData(name){
    // Puts the save into the dom to show saved filters and images
    $('div bg-info').removeClass('hide');
    $('#info-div').removeClass('hide');
    $('#info-span').text(`Sucessfully saved ${name}`);
}

async function submitImage(evt){
    // Submits the filter and image to be saved to the database
    $('#picture-name-form').toggleClass('hide');
    evt.preventDefault();
    data =  {
        'id' : $('#navbarDropdown').data('userid'),
        'name' : $('#picture-name').val(),
        'image' : $('#image').attr('src'),
        'ranges' : getSliderData(),
        'presets' : filters,
        'unsplash_id' : $('#canvas').data('unsplash')
    }
    resp = await axios.post(base_url + '/api/image/filter/new', {data: JSON.stringify(data)})
    // Show that the data got saved to the database
    showSavedData(data['name'])
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
        submitImage(evt);
    })
    $('#user-filters').change((evt)=>{
        handleUserFilters(evt.target.id);
    })
});