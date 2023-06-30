$(document).ready(function(){
    bindNavBtns(loginType);
})

//click detail button in search result table
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