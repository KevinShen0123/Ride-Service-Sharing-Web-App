$(document).ready(function(){
    bindNavBtns(loginType);
})

function click_detail_btn(request_id){
    window.location.href='/riderapp/reqdetail/'+request_id;
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