//import Swal from 'sweetalert2'
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

document.addEventListener('DOMContentLoaded', function() {
        increase_els = document.querySelectorAll('.increase_item')
        increase_els.forEach((increase_el)=>{
            increase_el.addEventListener('click', (e)=>{
                e.preventDefault();
                food_id = $(increase_el).attr('data-id');
                url = $(increase_el).attr('data-url');
                data = {
                    food_id : food_id,
                }
                $.ajax({
                        type: "GET",
                        url: url,
                        data: data,
                        success: function (response){
                            if(response.status =="Failed"){
                                new Swal()
                                Swal.fire({
                                 icon: "error",
                                  title: "Oops...",
                                text: response.message,
                                });
                            }
                            else if(response.status == "login_required"){
                                new Swal(response.message,"", "info").then(function (){
                                    window.location = "/login";
                                })
                            }
                            else{
                            $("#cart_counter").html(response.cart_counter["cart_count"]);
                            $("#qty_"+food_id).html(response.qty);
                            new Swal()
                            Swal.fire({
                            position: "top-end",
                            icon: "success",
                            title: response.message,
                            showConfirmButton: false,
                            allowOutsideClick: true,
                            allowEscapeKey: true,
                            backdrop: false,
                            timer: 1500
                            });
                            }
                            update_cart_amounts(subtotal=response.cart_amounts["subtotal"], taxes=response.cart_amounts["taxes"], grand_total=response.cart_amounts["grand_total"])
                        }
                })
            });
        });
        cart_item_els = document.querySelectorAll('.qty_item')
        cart_item_els.forEach((cart_item)=>{
            var data_qty = $(cart_item).attr("data-qty");
            var data_id = $(cart_item).attr("data-id");
            if(document.getElementById(data_id) != null){
                document.getElementById(data_id).innerHTML = data_qty;
            }
        })
        decrease_els = document.querySelectorAll('.decrease_item')
        decrease_els.forEach((decrease_el)=>{
            decrease_el.addEventListener('click', (e)=>{
                e.preventDefault();
                food_id = $(decrease_el).attr('data-id');
                url = $(decrease_el).attr('data-url');
                cart_id = $(decrease_el).attr('id');
                data = {
                    food_id : food_id,
                }
                console.log(data);
                $.ajax({
                        type: "GET",
                        url: url,
                        data: data,
                        success: function (response){
                            if(response.status == "Failed"){
                                console.log(response);
                                new Swal()
                                Swal.fire({
                                 icon: "error",
                                  title: "Oops...",
                                text: response.message,
                                });
                            }
                            else if(response.status == "login_required"){
                                new Swal(response.message,"", "info").then(function (){
                                    window.location = "/login";
                                })
                            }
                            else{
                            $("#cart_counter").html(response.cart_counter["cart_count"])
                            $("#qty_"+food_id).html(response.qty)
                            new Swal()
                            Swal.fire({
                            position: "top-end",
                            icon: "success",
                            title: response.message,
                            showConfirmButton: false,
                            allowOutsideClick: true,
                            allowEscapeKey: true,
                            backdrop: false,
                            timer: 1500
                            });
                            }
                            if(response.qty <= 0){
                                remove_cart_item(cart_id, 0)
                                
                            }
                            update_cart_amounts(subtotal=response.cart_amounts["subtotal"], taxes=response.cart_amounts["taxes"], grand_total=response.cart_amounts["grand_total"])
                        }
                })
            });
        });
        delete_cart_els = document.querySelectorAll('.delete_cart')
        delete_cart_els.forEach((delete_cart_el)=>{
            delete_cart_el.addEventListener('click',(e)=>{
                e.preventDefault();
                
                cart_id = $(delete_cart_el).attr('data-id');
                url = $(delete_cart_el).attr('data-url');
                data = {
                    cart_id : cart_id,
                }
                 $.ajax({
                        type: "GET",
                        url: url,
                        data: data,
                        success: function (response){
                            if(response.status == "Failed"){
                                console.log(response);
                                new Swal()
                                Swal.fire({
                                 icon: "error",
                                  title: "Oops...",
                                text: response.message,
                                });
                            }
                            else if(response.status == "login_required"){
                                new Swal(response.message,"", "info").then(function (){
                                    window.location = "/login";
                                })
                            }
                            else{
                            $("#cart_counter").html(response.cart_counter["cart_count"])
                            new Swal()
                            Swal.fire({
                            position: "top-end",
                            icon: "success",
                            title: response.message,
                            showConfirmButton: false,
                            timer: 1500
                            });
                            remove_cart_item(cart_id, 0);
                            update_cart_amounts(subtotal=response.cart_amounts["subtotal"], taxes=response.cart_amounts["taxes"], grand_total=response.cart_amounts["grand_total"])
                            }
                        }
                    })
            })
        })
    function remove_cart_item(cart_id, cart_item_qty){
        console.log(window.location.pathname)
        if(window.location.pathname == "/cart/"){
            if(cart_item_qty <= 0){
            document.getElementById("cart_item_"+cart_id).remove();
            check_cart_empty();
        }
        }
        
    }
    function check_cart_empty(){
        var cart_counter = document.getElementById("cart_counter").innerText;
        if(cart_counter == 0){
            var empty_el = document.getElementById("empty_cart");
            empty_el.style = "display: block;"
        }
        else{
            console.log("not Empty Cart")
        }
    }
function update_cart_amounts(subtotal , taxes, grand_total){
    if(window.location.pathname == "/cart/"){
    var subtotal_el = document.getElementById("subtotal");
    var tax_el = document.getElementById("tax");
    var total_el = document.getElementById("total");
    subtotal_el.innerText = subtotal;
    tax_el.innerText = taxes
    total_el.innerText = grand_total;
    

    }
}

    });