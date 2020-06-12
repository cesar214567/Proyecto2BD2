function Parallax(){
    
    $(document).ready(function(){
        $('.parallax').parallax();
      });
      document.addEventListener('DOMContentLoaded', function() {
        var elems = document.querySelectorAll('.parallax');
        var instances = M.Parallax.init(elems, options);
      });
}

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

function send(){
    var elem = document.getElementById('ttweets');
    clearInner(elem);
    var query = $('#busqueda').val();
    document.getElementById("busqueda").value = '';
    var msg = JSON.stringify({ "ID" : query, });
  // var query_keyword=query.split(" ");
  //  query=JSON.stringify(query_keyword);
  //  console.log(query);
    $.ajax({
        url:'/query',
        type:'POST',
        contentType: 'application/json',
        data : msg,
        dataType:'json',
        success: function(response){
            console.log(response);
            var i = 0;
            $.each(response, function(){            
            f = '<tr> <td> ID </td>  <td> Text </td> <td> Date </td> <td> Language </td>';
            f = f.replace( "ID", response[i].ID)
            f = f.replace( "Text", response[i].text)
            f = f.replace( "Date", response[i].date)
            f = f.replace( "Language", response[i].lang)
            i = i+1;
            $('#ttweets').append(f);
            });

            //alert(JSON.stringify(response));

        },
        error: function(response){
            alert(JSON.stringify(response));
            /*if (response['status']==401){
            document.getElementById('action').src = "/static/images/dislike.png";
            }else{
            document.getElementById('action').src = "/static/images/ok.png";
            var c="http://127.0.0.1:8080/static/chat.html";
            window.location=c;
            }*/
        }
    });



}


function eliminar(){
    $( "#desaparece").show();
    $.ajax({
        url:'/eliminar',
        type:'DELETE',
        contentType: 'application/json',
        dataType:'json',
        
        success: function(response){
            alert("Se han eliminado todos los bloques");
        },
        error: function(response){
            alert(JSON.stringify(response));
        }
    });
}

function createIndex(){
    
    var tema = $('#tema').val();
    document.getElementById("tema").value = '';
    var n_tweets=$('#N_Tweets').val();
    document.getElementById("N_Tweets").value = '';
    var size_block = $('#blocksize').val();
    document.getElementById("blocksize").value = '';
    document.getElementById("desaparece").value = ''; 
    var msg = JSON.stringify({ "n_tweets" : n_tweets, "tema" : tema , "blocksize": size_block });
    $.ajax({
        url:'/create',
        type:'POST',
        contentType: 'application/json',
        data : msg,
        dataType:'json',
        
        success: function(response){
            alert("Indice creado con el tema " + tema + " status: " + response.status);
            $( "#desaparece" ).hide();
            
            //alert(JSON.stringify(response));
        },
        error: function(response){
            alert(JSON.stringify(response));
            /*if (response['status']==401){
            document.getElementById('action').src = "/static/images/dislike.png";
            }else{
            document.getElementById('action').src = "/static/images/ok.png";
            var c="http://127.0.0.1:8080/static/chat.html";
            window.location=c;
            }*/
        }
    });
}

function invertedIndex(){
    var elem = document.getElementById('ttweets2');
    clearInner(elem);
    
    var query = $('#query').val();
    document.getElementById("query").value = '';
    
    var K = $('#K').val();
    document.getElementById("K").value = '';

    var msg = JSON.stringify({ "query" : query , "K":K});
    $.ajax({
        url:'/busqueda',
        type:'POST',
        contentType: 'application/json',
        data : msg,
        dataType:'json',
        
        success: function(response){
            console.log(response);
            var i = 0;
            $.each(response, function(){  
                console.log(response)          
                f = '<tr> <td> ID </td>  <td> Text </td> <td> Date </td> <td> Language </td>';
                f = f.replace( "ID", response[i].ID)
                f = f.replace( "Text", response[i].text)
                f = f.replace( "Date", response[i].date)
                f = f.replace( "Language", response[i].lang)
                i = i+1;
                $('#ttweets2').append(f);
            });
            //alert(JSON.stringify(response));
        },
        error: function(response){
            alert(JSON.stringify(response));
            /*if (response['status']==401){
            document.getElementById('action').src = "/static/images/dislike.png";
            }else{
            document.getElementById('action').src = "/static/images/ok.png";
            var c="http://127.0.0.1:8080/static/chat.html";
            window.location=c;
            }*/
        }
    });
}