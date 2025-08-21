let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        $("#id_pin_code").val("")
        var geocoder = new google.maps.Geocoder();
        var address = document.getElementById("id_address").value;
        geocoder.geocode({'address': address}, (results, status)=>{
             //console.log(results);
            // console.log(status);
            if(status == google.maps.GeocoderStatus.OK) 
            {
                var lattitude = results[0].geometry.location.lat();
                var longitude = results[0].geometry.location.lng();
                $("#id_lattitude").val(lattitude)
                $("#id_longitude").val(longitude)
                $("#id_address").val(address)
                place.address_components.forEach((address_component)=>{
                    address_component.types.forEach((type)=>{
                        //get country
                        if(type=="country"){
                            $("#id_country").val(address_component.long_name)
                        }
                        //get state
                        if(type=="administrative_area_level_1"){
                            $("#id_state").val(address_component.long_name)
                        }
                        //get city
                        if(type=="locality"){
                            $("#id_city").val(address_component.long_name)
                        }
                        //get pin code postal_code
                         if(type=="postal_code"){
                            $("#id_pin_code").val(address_component.long_name)
                        }
                    })
                })
            }
        })
    }
    // get the address components and assign them to the fields
}
