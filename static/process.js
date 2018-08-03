//function process() {
    
    function process_start() {
        console.log("process_start function waiting for click");
        
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
                    console.log(data.loginVvalid);
                    console.log('valid')
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
                            'background-color': '#2e86de'
                            //'background': 'linear-gradient(green, blue)'
                        });
                        
                        setTimeout(function() {
                            console.log("process_progress called from start process"); //debugging
                            process_progress(data.key); //uses key from json object returned from _start_process
                        }, 100);
                        
                    });
                }

            })

            
            //potentially replace with jquery addclass (preconfigured class with progressbar properties)
            // in css, this would be "#processStart div" (jquery needs the >)
            
            
            
            
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
            $('.detailMonitorTopData:eq(2)').text(data.time + "s");
            $('.detailMonitorTopData:eq(3)').text(data.operation);
            
            if(data.command == prev_command){
                prev_command = data.command;
                //console.log("command is the same")
            }
            else{
                $('#solverOutput').append("OUT: " + data.command + "\n");
                prev_command = data.command;
                //console.log("command has changed")
            }
            
            
            
            if (!data.done) {
                setTimeout(function() {
                    process_progress(data.key);
                }, 100);
            }
            else {
                $('#processStart').removeAttr('disabled');
                //$('#progress').progressbar('option', 'value', 0);
                //$('#progress').progressbar('option', 'disabled', true);
            }
        });
    }
 
    
    function check_link() {
        console.log("this function will report if link is valid by calling function in list_solver or elsewhere to see if link is valid");
    }

    function check_login() {
        console.log("this function will report back whether or not the entered credentials are valid");
        /*if returns false, show outputfield to view error message
        may have to rely on alternate dummy object. EITHER THAT or the process_progress/process_start waits to initialize other functionality
        until these functions return true*/
    }


    function alert_test(percent) {
        
        $('#processStart').click(function() {
            $('#processStart a').hide();
            $('#processStart').progressbar({value: 30});
            /*$('#leftBlock').css({
                'background-image': 'url(../resources/images/POtJ.gif)',
                //'background-color': 'green'
            }); */
            
            
        })
    }


    function init() {
        
        //$('#processStart').progressbar({'disabled': true});
        //console.log("assigned progress bar")
        process_start();
        console.log('start_process called...waiting for initiation...');
        
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