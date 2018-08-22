//function process() {
    
    function process_start() {
        //console.log("process_start function waiting for click");
        
        $('#processStart').click(function() {
            
            //disable button (potentially place these into a function)
            $('#processStart').prop('disabled', true)
            $('#processStart').progressbar({enabled: true});
            $('#processStart').progressbar({value: false});
            $('#processStart').css({'height': '40px'});
            $('#processStart a').hide();
            $('#detailButton').fadeIn(1000);
            $('.detailMonitorTopData:eq(3)').text("validating list link and credentials");

            //var errorArray = $('.errorField').toArray();
            $('.errorField').each(function() {
                $(this).text("");
            });
            // CALL ON NEW VALIDATION FUNCTION HERE .GETJSON.
            // ADD VALIDATION APP ROUTE IN MAIN.PY
            $.getJSON('/_validate', {
                'username' : $('#userField').val(),
                'password' : $('#passField').val(),
                'link' : $('#linkField').val()
            },
            function(data) {
                if(!data.loginValid || !data.linkValid) {
                    
                    //re-enable start button and destroy progressbar
                    $('#processStart').progressbar("destroy");
                    $('#processStart').css({'height': '80px'});
                    $('#processStart a').show();
                    $('#processStart').prop('disabled', false)

                    //rehide detail access
                    $('#detailButton').hide();
                    $('#detailMonitor').hide();

                    //report error message on page
                    if(!data.loginValid) {
                        $('.errorField:eq(1)').text("*** provided username/password invalid")
                    }
                    if(!data.linkValid) {
                        $('.errorField:eq(0)').text("*** link provided not valid. Check FAQ to ensure correct link provided")
                    }
                }
                else {
                    // make separate start_process function for this section
                    $.getJSON('/_start_process', {
                        'list_link' : $('#linkField').val(),
                        'email' : $('#emailField').val(),
                        'username' : $('#userField').val(),
                        'password' : $('#passField').val()
                    },
                    function(data) {
                        
                        $('#processStart').attr('disabled','disabled');
                        $('#processStart').progressbar('option', 'disabled', false);
                        $('#processStart').progressbar('option', 'value', data.percent);
                        
                        $('#processStart > div').css({
                            'background': '#55efc4'
                            //'background': 'linear-gradient(green, blue)'
                        });
                        
                        setTimeout(function() {
                            //console.log("process_progress called from start process"); //debugging
                            process_progress(data.key); //uses key from json object returned from _start_process
                        }, 100);
                        
                    });
                }

            })
            return false;  
            
        });
    }
    

    var prev_command = ""
    function process_progress(key) {
        
        //second parameter is what program can request using request.args.get
        //give _process_progress key to look for object (in dictionary form? { : }) (callback value)
        //Only check for process_progress function and separate other functionality into auxillary functions
        $.getJSON('/_process_progress', {'key': key},
                  
        function(data) {
            $('#processStart').progressbar('option', 'value', data.percent);
            $('.detailMonitorTopData:eq(0)').text(data.words);
            $('.detailMonitorTopData:eq(1)').text(data.percent + "%");
            //add if structure here to switch to minutes
            //$('.detailMonitorTopData:eq(2)').text(data.time + "s");
            $('.detailMonitorTopData:eq(3)').text(data.operation);
            
            if(data.time >= 60) {
                var time = Math.round(data.time / 60);
                $('.detailMonitorTopData:eq(2)').text(time + "m");
            }
            else {
                $('.detailMonitorTopData:eq(2)').text(data.time + "s");
            }
            
            
            if(data.command == prev_command){
                prev_command = data.command;
                //console.log("command is the same")
            }
            else{
                $('#solverOutput').append("OUT: " + data.command + "\n");
                prev_command = data.command;
                //console.log("command has changed")
            }
            
            
            // if not yet completed
            if (!data.done) {
                setTimeout(function() {
                    process_progress(data.key);
                }, 100);
            }
            // if completed
            // possible add check for whether results sent or not
            else {
                //$('#processStart').removeAttr('disabled');
                //$('#progress').progressbar('option', 'value', 0);
                //$('#progress').progressbar('option', 'disabled', true);
                //re-enable start button and destroy progressbar
                 $('#processStart').progressbar("destroy");
                 $('#processStart a').css({'color': '#2e86deff'});
                 $('#processStart').css({'background-color': '#55efc4'});
                 $('#processStart a').show();
                 $('#processStart').css({'height': '80px'});
                 $('#processStart a').css({'color': 'white'});
                 $('#processStart a').text("Completed");
                 
                 $('.detailMonitorTopData:eq(3)').text("Completed");
                 $('#solverOutput').append("OUT: " + "results sent" + "\n");
                 
            }
        });
    }


    function init() {
        
        //$('#processStart').progressbar({'disabled': true});
        //console.log("assigned progress bar")
        process_start();
        //console.log('start_process called...waiting for initiation...');
        
        $('#detailButton').hide();
        $('#detailMonitor').hide();
        //$('#detailMonitor').css({'height': '0px'});
        
        $('#detailButton').click(function(){
            //$('.trigger:visible').hide();
            if($('#detailMonitor').is(":hidden") == true) {
                $('#detailMonitor').fadeIn(0.2);
                $('#detailButton').text('Hide Details');
            }
            else {
                $('#detailMonitor').fadeOut(0.2);
                $('#detailButton').text('Show Details');
            }
        });
    }
    
    /*return {
        init: function() {
            
            
        }
    }*/
//};


$(function() {
    init();
    //alert_test(20)
});










 /*
                        if(!data.logValid) { //or linkValid
        
                            $('#processStart').progressbar("destroy");
                            $('#processStart').css({'height': '80px'});
                            $('#processStart a').show();
                            $('#processStart').prop('disabled', false)
        
                            if(!data.loginValid) {
                                $('.errorField:eq(1)').text("*** provided username/password invalid")
                            }
                            else if(!data.linkValid) {
                                
                            }
                        } */