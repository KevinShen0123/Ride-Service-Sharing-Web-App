$(document).ready(function(){
    var whichAddress = null;
    bindNavBtns(loginType);

    $("#address-from").click(function(){
        whichAddress = 'from';
        clearAddressInput();
        $("#address-modal").modal('show');
    })

    $("#address-to").click(function(){
        whichAddress = 'to';
        clearAddressInput();
        $("#address-modal").modal('show');
    })

    $("#btn-search-req").click(function(){
        $("#ra-form-search form").submit();
    })

    $("#btn-address-input").click(function(){
        let state = $("#address-state").val();
        let city = $("#address-city").val();
        let addressDetail = $("#address-detail").val();
        if(state == '' || city == '' || addressDetail == ''){
            alert('Address cannot be empty');
            return;
        }
        let address = addressDetail + ', ' + city + ', ' + state;
        if(whichAddress == 'from'){
            $("#address-from").val(address);
        }else if(whichAddress == 'to'){
            $("#address-to").val(address);
        }else{
            console.log("whichAddress is null");
        }
    });

    $("#btn-new-request").click(function(){
        $("#new-request").modal('show');
    });

    $("#btn-submit-request").click(function(){
        let f_state = $("#input-boarding-state").val();
        let f_city = $("#input-boarding-city").val();
        let f_address = $("#input-boarding-address").val();
        let t_state = $("#input-destination-state").val();
        let t_city = $("#input-destination-city").val();
        let t_address = $("#input-destination-address").val();
        if(f_state=='' || f_city=='' || f_address==''||t_state=='' || t_city=='' || t_address==''){
            alert('Address cannot be empty');
            return;
        }

        let boarding = f_address + ', ' + f_city + ', ' + f_state;
        let destination = t_address + ', ' + t_city + ', ' + t_state;
        let arrival_time = $("#arrivalTime").val();
        let passenger_number = $("#passenger-number").val();
        let vehicle_type = $("#vehicle-type option:selected").val();
        let allow_share = $("#allow-share option:selected").val();
        let specific = $("#specific").val();
        if(arrival_time == ''){
            alert("Arrival time cannot be empety");
            return;
        }
        if(passenger_number == ''){
            alert('Passenger number cannot be empty');
            return;
        }
        
        let data = {
            'boarding': boarding,
            'destination': destination,
            'arrival_time': arrival_time,
            'psnumbers': passenger_number,
            'vehicle_tid': vehicle_type,
            'canshare': allow_share,
            'specific': specific,
            'csrfmiddlewaretoken': CSRF_TOKEN
        };
        $.post('/riderapp/rider/new_request', data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                location.reload();
            }else{
                console.log('Request failed.');
            }
        })
    });
})

//clear address input
function clearAddressInput(){
    $("#address-state").val('');
    $("#address-city").val('');
    $("#address-detail").val('');
}

//click detail button in Current Comfirmed Requests table
function click_detail_btn(detid){
    window.location.href='/riderapp/reqdetail/'+detid;
}

//bind buttons in the navigation bar
function bindNavBtns(loginType){
    $("#nav-account").click(function(){
        window.location.href='/riderapp/personal/'+id;
    });

    $("#nav-index").click(function(){
        if(loginType == 'd'){
            window.location.href = '/riderapp/driver/index';
        }else{
            window.location.href = '/riderapp/rider/index';
        }
    });
}