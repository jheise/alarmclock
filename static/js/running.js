//handle stopping running alarms
function loadRunning(){
    var contain = $("#active-display");
    $.get("../running_alarms", function(content){
        var data = $.parseJSON(content);
        for( x in data){
            console.log( "x is " + data[x]);
            contain.append("<button type='button' id="+data[x]+">Stop Alarm</button>");
            $("#"+data[x]).click(function(event){
                var target = $(this).parent();
                $.get('../kill/'+data[x], function(content){
                    var data = $.parseJSON(content);
                    console.log(data);
                });
            });
        }
    });
}
