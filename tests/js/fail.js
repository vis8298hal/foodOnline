function fail_test_check(){
url = "/marketplace/add_to_cart/15"
data = {food: "15"}
out = $.ajax({
                        type: "GET",
                        url: url,
                        data: data,
                        success: function (response){
                            console.log(response);
                        }
                })
console.log(out)
}