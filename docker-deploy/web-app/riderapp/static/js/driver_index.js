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
        let address = addressDetail + ', ' + city + ', ' + state;
        if(whichAddress == 'from'){
            $("#address-from").val(address);
        }else if(whichAddress == 'to'){
            $("#address-to").val(address);
        }else{
            console.log("whichAddress is null");
        }
    })
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