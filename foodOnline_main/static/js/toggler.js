    function make_veg_toggle(){
        document.querySelector('.toggle_ball_item').classList.add("veg")
        document.querySelector('.toggle_ball_item').classList.remove("non_veg")
        document.getElementById("id_is_veg").checked = true;
        
        document.querySelector(".buyer-logged-in").style = "background-color: rgba(0,60,0, 0.5);"

    }
    function make_nonveg_toggle(){
        document.querySelector('.toggle_ball_item').classList.remove("veg")
        document.querySelector('.toggle_ball_item').classList.add("non_veg")
        document.getElementById("id_is_veg").checked = false;
        document.querySelector(".buyer-logged-in").style = "background-color: rgba(60, 6, 0, 0.38);"
    }
    function start_animation(){
        toggle_ball_item = document.querySelector('.toggle_ball_item');
        has_veg = toggle_ball_item.classList.contains("veg");
        has_non_veg = toggle_ball_item.classList.contains("non_veg")
        if(has_veg){
            make_nonveg_toggle();
        }
        else if(has_non_veg){
            make_veg_toggle()
        }
        else{
            sync_with_toggle()
        }
    }
    function load_and_toggle(){
        const active_status = document.getElementById("id_is_veg");
        if (active_status.checked) {
            make_veg_toggle();
        } 
        else {
            make_nonveg_toggle();
        }
    }
    function sync_with_toggle(){
        load_and_toggle()
    }
sync_with_toggle()