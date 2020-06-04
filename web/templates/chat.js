function clearInner(node) {
  while (node.hasChildNodes()) {
    clear(node.firstChild);
  }
}

function clear(node) {
  while (node.hasChildNodes()) {
    clear(node.firstChild);
  }
  node.parentNode.removeChild(node);
  }

function hidden(){
    $('#container').hide();
}

function whoami(){
        $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){

                $('#cu_username').html(response['username'])
                var name = response['name']+" "+response['fullname'];
                $('#cu_name').html(name);
                yo=response['id'];
                allusers(yo);
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }

    function allusers(yo){
        $.ajax({
            url:'/users',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));
                var i = 0;
                $.each(response, function(){

                if (response[i].id!=yo){
                    f = '<div><a href="#" class="collection-item" onclick="get_messages('+response[i].id+','+yo+')">'+response[i].username+'</a></div>';
                    i = i+1;
                    $('#allusers').append(f);
                }else{
                i=i+1;
                }
                });
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }
    function get_messages(persona,yo){
    $('#container').show();
    var n = document.getElementById("hola");
        clearInner(n);
        $.ajax({
            url:'/message',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));
                var i = 0;

                $.each(response, function(){
                if ((response[i].user_from_id==yo & response[i].user_to_id==persona)| (response[i].user_from_id==persona & response[i].user_to_id==yo)){
                    if (response[i].user_from_id==yo){
                        f = '<div class="right-align"><div><h4>'+response[i].content+'</div></h4><div>'+response[i].sent_on+'</div> </div>';
                        i = i+1;
                        $('#hola').append(f);
                }else{
                f = '<div class="left-align"><div><h3>'+response[i].content+'</div></h3><div>'+response[i].sent_on+'</div></div>';
                i = i+1;
                $('#hola').append(f);
                }
                }else{
                i=i+1;
                }});
                var x=document.getElementById('boton');
                clearInner(x);
                var a='<div class="row" id="buttonsend"><div class="col s12"><div class="row">';
                a+='<div class="input-field col s10">';
                a+='<input type="text" id="autocomplete-input" class="">';
                a+='<label for="autocomplete-input"></label></div><div class="col s2"><br>';
                a+='<a class="waves-effect waves-light btn" onclick="send('+persona+','+yo+')">send';
                a+='</button></div></div></div></div>';
                $('#boton').append(a);
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }

function send(persona,yo){
    var content= $('#autocomplete-input').val();
    if (content!=''){
    var message = JSON.stringify({
        "content": content,
        "user_from_id": yo,
        "user_to_id": persona,
        });
    $.ajax({
            url:'/messages',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json'

        });

    get_messages(persona,yo);
}}