$(document).ready(function(){
    bindNavBtns(loginType);
    handleRequestByStatus(req_status, req_owner, myRole, myId, req_driverId, loginType, req_id);
    bindBasicModifyBtns();
    if(canmodify == '1'){
        $(".div-btn-modify").css("display","block");
        var whichAddr = null;
        bindModifyBtns(req_id, myId);
    }

    //driver stop comfirming
    $("#btn-driver-stop-comfirmed").click(function(){
        let data = {
            'request_id': req_id,
            'csrfmiddlewaretoken': CSRF_TOKEN
        };

        $.post('/riderapp/reqdetail/stop_comfirmed', data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                location.reload();
            }else{
                alert(info['errmsg'])
                location.reload();
            }
        });
    });
    
})

function clearAddrInput(){
    $("#address-state").val('');
    $("#address-city").val('');
    $("#address-detail").val('');
}

//bind boarding, destination and arrival time
function bindBasicModifyBtns(){
    $("#btn-address-modify").click(function(){
        let state = $("#address-state").val();
        let city = $("#address-city").val();
        let detail = $("#address-detail").val();
        if(state == '' || city == '' || detail == ''){
            alert('Address cannot be empty');
            return;
        }
        let address = detail + ', ' + city + ', ' + state
        if(whichAddr == 'from'){
            modifyRequestBasicInfo('boarding', address, req_id, myId);
        }else if(whichAddr == 'to'){
            modifyRequestBasicInfo('destination', address, req_id, myId);
        }
    });

    $("#btn-arrival-time-modify").click(function(){
        let arrivalTime = $("#arrival-time").val();
        if(arrivalTime == ''){
            alert('Arrival time cannot be empty');
            return;
        }
        modifyRequestBasicInfo('arrival_time', arrivalTime, req_id, myId);
    });
}

function bindModifyBtns(req_id, myId){
    //buttons in the detail page
    $("#btn-modify-boarding").click(function(){
        clearAddrInput();
        whichAddr = 'from';
        $("#address-modal").modal('show');
    });

    $("#btn-modify-destination").click(function(){
        clearAddrInput();
        whichAddr = 'to';
        $("#address-modal").modal('show');
    });

    $("#btn-modify-arrival-time").click(function(){
        $("#arrival-time-modal").modal('show');
    });

    // $("#btn-modify-psnumber").click(function(){
    //     $("#passenger-number-modal").modal('show');
    // });

    $("#btn-modify-vehicle-tid").click(function(){
        $("#vehicle-type-modal").modal('show');
    });

    $("#btn-modify-specific").click(function(){
        $("#specific-modal").modal('show');
    });

    //sharing switch button
    $("#btn-change-to-no-share").click(function(){
        modifyRequestBasicInfo('canshare', '0', req_id, myId);
    });

    $("#btn-change-to-share").click(function(){
        modifyRequestBasicInfo('canshare', '1', req_id, myId);
    });

    //buttons in the modify page

    $("#btn-vtype-modify").click(function(){
        let vtype = $("#select-vehicle-type option:selected").val();
        modifyRequestBasicInfo('vehicle_tid', vtype, req_id, myId);
    });

    $("#btn-specific-modify").click(function(){
        let specific = $("#text-specific").val();
        modifyRequestBasicInfo('specific', specific, req_id, myId);
    });

    $("#btn-passenger-number-modify").click(function(){
        let party_number = $("#passenger-number").val();
        if(party_number == ''){
            alert('Party number cannot be empty');
            return;
        }
        modifyRequestBasicInfo('party_number', party_number, req_id, myId);
    });
}

function modifyRequestBasicInfo(fieldName, fieldVal, request_id, myId){
    let data = {
        'request_id': request_id,
        'fieldName': fieldName,
        'fieldVal': fieldVal,
        'myId': myId,
        'csrfmiddlewaretoken': CSRF_TOKEN
    };
    $.post('/riderapp/reqdetail/modify', data, function(res){
        let info = $.parseJSON(res);
        if(info['status'] == '1'){
            location.reload();
        }else{
            alert(info['errmsg']);
            location.reload();
        }
    });
}

// Handle request by status
// @param status request status, required
// @param owner request owner id, required
// @param myRole my role, required
// @param myId my id, required
// @driverId driver id of that request, if status>0, required, else None
// @param loginType 'd'/'r', login as driver or rider
function handleRequestByStatus(status, owner, myRole, myId, driverId, loginType, req_id){
    //completed request, visited from history
    if(status == '2'){
        $("#btn-request-opt").text('Completed');
        $("#btn-request-opt").css('cursor','auto');
        return;
    }
    if(loginType == 'd' && myRole == '1'){
        //I am driver now
        if(status == '0'){
            //status: open
            comfirmRequest(req_id, myId);
        }else if(status == '1' && driverId == myId){
            //status: comfirmed
            completeRequest(req_id, myId);
        }
    }else{
        //I am rider now
        if(status == '0'){
            //status: open
            if(owner == myId){
                cancelRequest(req_id, myId);
            }else{
                joinRequest(req_id, myId);
            }
        }else if(status == '1'){
            //for no driver, nothing can do for comfirmed request
            $("#btn-request-opt").text('Comfirmed');
            $("#btn-request-opt").css('cursor','auto');
        }
    }
}

function cancelRequest(req_id, myId){
    $("#btn-request-opt").text('Cancel');
    $("#btn-request-opt").click(function(){
        let data = {
            'request_id': req_id,
            'owner_id': myId,
            'csrfmiddlewaretoken': CSRF_TOKEN
        };
        $.post('/riderapp/reqdetail/cancel',data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                window.location.href="/riderapp/rider/index";
            }else{
                alert(info['errmsg']);
                location.reload();
            }
        })
    })
}

function comfirmRequest(req_id, myId){
    $("#btn-request-opt").text('Comfirm');
    $("#btn-request-opt").click(function(){
        let data = {
            'request_id': req_id,
            'driver_id': myId,
            'csrfmiddlewaretoken': CSRF_TOKEN
        };
        $.post('/riderapp/reqdetail/comfirm', data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                location.reload();
            }else{
                alert(info['errmsg']);
                location.reload();
            }
        })
    })
}

function joinRequest(req_id, myId){
    if(issharer == '1'){
        $("#btn-request-opt").text('Joined');
        $("#btn-request-opt").css('cursor','auto');
        return;
    }
    $("#btn-request-opt").text('Join');
    $("#btn-request-opt").click(function(){
        $("#party-number-modal").modal('show');
    });

    $("#btn-party-number-set").click(function(){
        let party_number = $("#party-number").val();
        if(party_number == ''){
            alert('Party number cannot be empty');
            return;
        }
        let data = {
            'request_id': req_id,
            'sharer_id': myId,
            'csrfmiddlewaretoken': CSRF_TOKEN,
            'party_number': party_number
        };
        $.post('/riderapp/reqdetail/join', data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                location.reload();
            }else{
                alert(info['errmsg']);
                window.location.href="/riderapp/rider/index";
            }
        });
    });
}

function completeRequest(req_id, myId){
    $("#btn-request-opt").text('Complete');
    $("#btn-request-opt").click(function(){
        let data = {
            'request_id': req_id,
            'driver_id': myId,
            'csrfmiddlewaretoken': CSRF_TOKEN
        };
        $.post('/riderapp/reqdetail/complete', data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                window.location.href="/riderapp/driver/index";
            }else{
                alert(info['errmsg']);
                location.reload();
            }
        });
    })
}

function modifyPartyNumber(){
    $("#passenger-number-modal").modal('show');
}

function deleteRider(delUserId, request_id){
    let data = {
        'del_id':delUserId,
        'request_id':request_id,
        'csrfmiddlewaretoken': CSRF_TOKEN
    };
    $.post('/riderapp/reqdetail/delete', data, function(res){
        let info = $.parseJSON(res);
        if(info['status'] == '1'){
            location.reload();
        }else{
            alert(info['errmsg']);
            location.reload();
        }
    });
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