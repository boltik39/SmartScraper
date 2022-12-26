function update_messages(messages){
    $("#messages-content").html("");
    $.each(messages, function (i, m) {
        $("#messages-content").append("<div class='alert "+m.extra_tags+" alert-dismissible' role='alert' style='margin: 15px 15px 0px -15px;'>"+m.message+"</div>");
    });
}

var frm = $("#addForm"); /// adding devices messages
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
frm.submit(function (e) {
    e.preventDefault();

    $.ajax({
        url: frm.attr('action'),
        type: frm.attr('method'),
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: frm.serialize(),
        success:function(data){
            console.log(data.messages);
            update_messages(data.messages);
            frm.each(function(){
                this.reset();
            });
        },
        error:function(data){
            console.log('error')
        },
    });
});

$(document).ready(function(){ /// delete func
    $("#delete_id").click(function(){
        if (confirm("Are you sure to delete these items?")){
            var id = [];
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $(':checkbox:checked').each(function(i){
                id[i]=$(this).val()
            })
            if (id.length==0){
                alert("You don't choose items. Try again.")
            }else{
                console.log(id)
                $.ajax({
                    url:"delete",
                    type:"POST",
                    headers:{
                    "X-CSRFToken": csrftoken
                },
                    data:{
                        id,
                    },
                    success:function(response){
                        for (var i=0; i < id.length; i++){
                            $('tr#'+id[i]+'').css('background-color', '#ccc');
                            $('tr#'+id[i]+'').fadeOut('slow');
                        }
                    }
                })
            }
        }
    })
})