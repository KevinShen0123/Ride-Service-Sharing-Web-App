$(document).ready(function(){
    var registerAs = 0;

    //click register label
    $("#btn-register").click(function(){
        $("#login-container").css('display','none');
        $("#register-container").css('display','block');
    });

    //click register as driver label
    $("#btn-register-driver").click(function(){
        registerAs = 1;
        $("#register-driver-notice").css('display','none');
        $("#inputs-vehicle-info").css('display','block');
    });
    
    //click register button
    $("#btn-register-submit").click(function(){
        register(registerAs);
    })

    //click login button
    $("#btn-login").click(function(){
        let username = $("#username").val();
        let password = $("#password").val();
        let loginType = $("#login-as-radios input:radio:checked").val();
        if(username == '' || password == ''){
            alert('Username and password cannot be empty');
            return;
        }
        let data = {
            'username': username,
            'password': password,
            'loginType': loginType,
            'csrfmiddlewaretoken': CSRF_TOKEN
        };
        $.post('/riderapp/try_login', data, function(res){
            let info = $.parseJSON(res);
            if(info['status'] == '1'){
                //jump to index page based on rider or driver
                let role = info['role'];
                if(role == 0 && loginType == '1'){
                    //rider want to inter driver page
                    alert('Please register as a driver first.');
                }else{
                    //login success
                    if(loginType == '1'){
                        //driver index
                        window.location.href = '/riderapp/driver/index';
                    }else{
                        window.location.href = '/riderapp/rider/index';
                    }
                }
            }else{
                alert('Password or username error, please try again.');
            }
        });
    });
});

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

function register(registerAs){
    let username = $("#reg-username").val();
    let email = $("#reg-email").val();
    let passwd = $("#reg-password").val();
    let retypePasswd = $("#reg-retype-password").val();
    if(username == '' || email == '' || passwd == '' || retypePasswd == ''){
        alert('username, email and password cannot be empty');
        return;
    }
    if(!validate(email, 'email')){
        alert('Email is not valid');
        return;
    }
    if(passwd != retypePasswd){
        alert('The passwords entered two times are inconsistent');
        return;
    }
    if(!validate(passwd, 'password')){
        alert('Password needs to contain at least 8-16 characters, at least 1 uppercase letter, 1 lowercase letter and 1 number');
        return;
    }
    let data = {
        'username':username,
        'email':email,
        'password':passwd,
        'role': registerAs,
        'csrfmiddlewaretoken': CSRF_TOKEN
    };
    //register as driver
    if(registerAs == 1){
        let name = $("#reg-name").val();
        let licensePlateNumber = $("#reg-license-plate-number").val();
        let vehicleType = $("#register-vehicle-type option:selected").val();
        let maxPassnumber = $("#register-max-passenger").val();
        let specific = $("#register-text-specific").val();
        if(name == ''){
            alert('Name cannot be empty');
            return;
        }
        if(licensePlateNumber == ''){
            alert('License plate number cannot be empty');
            return;
        }
        if(maxPassnumber == ''){
            alert('Max passenger number cannot be empty');
            return;
        }

        data['name'] = name;
        data['license_plate_number'] = licensePlateNumber;
        data['max_numbers'] = maxPassnumber;
        data['specific'] = specific;
        data['vehicle_tid'] = vehicleType;
    }
    $.post('/riderapp/register', data, function(res){
        let info = $.parseJSON(res);
        if(info['status'] == '1'){
            location.reload();
        }else{
            if(info['username'] == '1'){
                alert('Username already exists')
                return;
            }
            console.log('Register failed.');
        }
    });
    
}