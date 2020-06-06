function Parallax(){
    
    $(document).ready(function(){
        $('.parallax').parallax();
      });
      document.addEventListener('DOMContentLoaded', function() {
        var elems = document.querySelectorAll('.parallax');
        var instances = M.Parallax.init(elems, options);
      });
}

function send(){
    var query = $('#textarea1').val();
    var query_keyword=query.split("");
    query=JSON.stringify(query_keyword);
    console.log(query);
    $.ajax({
        url:'/query',
        type:'POST',
        contentType: 'application/json',
        data : query,
        dataType:'json',
        success: function(response){
            alert(JSON.stringify(response));

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

