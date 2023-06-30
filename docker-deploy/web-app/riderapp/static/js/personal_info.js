$(document).ready(function(){
    bindNavBtns(loginType);
    var whichSimple = null;
    var userId = id;
    bindModifyBtns();
    bindSaveBtns(userId);

    //judge if to show history footer by login type
    if(loginType == 'r'){
        $("#card-footer-rider").css("display","block");
    }

    //click register to driver button
    $("#btn-register-driver").click(function(){
        $("#register2Driver").modal('show');
    });

    //click stop being a driver button
    $("#btn-cancel-driver").click(function(){
        $.get('/riderapp/personal/stopdriver', function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                window.location.href="/riderapp/rider/index";
            }else{
                console.log('cancel failed.')
            }
        })
    });

    //click submit new password button
    $("#btn-submit-pwd").click(function(){
        let oldpwd = $("#input-old-pwd").val();
        let newpwd = $("#input-new-pwd").val();
        let retypepwd = $("#input-retype-pwd").val();
        if(oldpwd == '' || newpwd == '' || retypepwd == ''){
            alert('Input cannot be empty');
            return;
        }

        if(newpwd != retypepwd){
            alert('The passwords entered two times are inconsistent');
        }else if(!validate(newpwd, 'password')){
            alert('Password needs to contain at least 8-16 characters, at least 1 uppercase letter, 1 lowercase letter and 1 number');
        }else{
            changePwd(oldpwd, newpwd, userId);
        }
    });

    //click register driver button
    $("#btn-submit-register").click(function(){
        let name = $("#register-name").val();
        if(name == ''){
            alert('Name cannot be empty');
            return;
        }
        let license_plate_number = $("#register-license-num").val();
        if(license_plate_number == ''){
            alert('License plate number cannot be empty');
            return;
        }
        let vehicle_tid = $("#register-vehicle-type option:selected").val();
        let max_numbers = $("#register-max-passenger").val();
        if(max_numbers == ''){
            alert('Max passenger number cannot be empty');
            return;
        }
        let specific = $("#register-text-specific").val();
        registerDriver(name, license_plate_number, vehicle_tid, max_numbers, specific, userId);
    });

    //click footer of personal information
    $("#footer-to-request-history").click(function(){
        window.location.href='/riderapp/reqhistory/'+userId+'/r';
    });

    //click footer of driver information
    $("#footer-driver-history").click(function(){
        window.location.href='/riderapp/reqhistory/'+userId+'/d';
    });
})

// send register info to server
function registerDriver(name, license_plate_number, vehicle_tid, max_numbers, specific, userId){
    let data = {
        'name': name,
        'license_plate_number': license_plate_number,
        'vehicle_tid': vehicle_tid,
        'max_numbers': max_numbers,
        'specific': specific,
        'user_id': userId,
        'csrfmiddlewaretoken': CSRF_TOKEN
    };
    $.post('/riderapp/personal/register', data, function(res){
        let info = $.parseJSON(res);
        if(info['status'] == '1'){
            location.reload();
        }else{
            alert('Register failed. Error occurs in server');
        }
    });
}

function changePwd(oldpwd, newpwd, userId){
    let data = {
        'userId': userId,
        'oldpwd': oldpwd,
        'newpwd': newpwd,
        'csrfmiddlewaretoken': CSRF_TOKEN
    }
    $.post('/riderapp/personal/password', data, function(res){
        let info = $.parseJSON(res);
        if(info['status'] == '1'){
            $("#modify-password").modal('hide');
            alert('Password reset successfully.');
        }else{
            alert('The old password is not valid.');
        }
    });
}

function clickSimpleModifyBtn(fieldname){
    whichSimple = fieldname;
    $("#input-modify-simval").val('');
    $("#modify-simple-value").modal('show');
}

function bindModifyBtns(){
    $("#mf-btn-username").click(function(){
        clickSimpleModifyBtn('username');
    });
    $("#mf-btn-email").click(function(){
        clickSimpleModifyBtn('email');
    });
    $("#mf-btn-pwd").click(function(){
        $("#modify-password").modal('show');
    });
    $("#mf-btn-name").click(function(){
        clickSimpleModifyBtn('name');
    });
    $("#mf-btn-lpn").click(function(){
        clickSimpleModifyBtn('license_plate_number');
    });
    $("#mf-btn-mpn").click(function(){
        $("#modify-max-passnumber").modal('show');
    });
    $("#mf-btn-vtype").click(function(){
        $("#modify-vehicle-type").modal('show');
    })
    $("#mf-btn-specific").click(function(){
        $("#modify-specific").modal('show');
    })
}

// veryfy if input is valid
function validate(input, fieldName){
    let reg = null;
    if(fieldName == 'email'){
        reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
    }else if(fieldName == 'password'){
        reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,16}$/;
    }
    if(reg != null && !reg.test(input)){
        return false;
    }
    return true;
}

function bindSaveBtns(userId){
    $("#btn-save-simple").click(function(){
        let val = $("#input-modify-simval").val();
        sendModification(whichSimple, val, userId);
    });

    $("#btn-save-mpn").click(function(){
        let val = $("#modify-max-passenger").val();
        sendModification('max_numbers', val, userId);
    })

    $("#btn-save-vtype").click(function(){
        let val = $("#modify-vehicle-type option:selected").val();
        sendModification('vehicle_tid', val, userId);
    })

    $("#btn-save-specific").click(function(){
        let val = $("#text-specific").val();
        sendModification('specific', val, userId);
    })
}

// Send modification to server except password
function sendModification(fieldname, fieldVal, userId){
    if(!validate(fieldVal, fieldname)){
        alert('Input ' + fieldname + ' is not valid');
        return;
    }
    let data = {
        'fieldName': fieldname,
        'fieldVal': fieldVal,
        'userId': userId,
        'csrfmiddlewaretoken': CSRF_TOKEN
    }
    $.post('/riderapp/personal/modify', data, function(res){
        let info = $.parseJSON(res);
        if(info['status'] == '1'){
            location.reload();
        }else{
            alert('You still have unfinished requests, please finish them first!');
        }
    })
}

//bind buttons in the navigation bar
function bindNavBtns(loginType){
    $("#nav-log-out").click(function(){
        $.get('/riderapp/log_out', function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                window.location.href='/riderapp/login'
            }else{
                console.log('Log out failed');
            }
        });
    });

    $("#nav-index").click(function(){
        if(loginType == 'd'){
            window.location.href = '/riderapp/driver/index';
        }else{
            window.location.href = '/riderapp/rider/index';
        }
    });
}