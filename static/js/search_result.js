function update_messages(messages){ 
    /// creates messages-notifications when adding a device
    $("#messages-content").html("");
    $.each(messages, function (i, m) {
        $("#messages-content").append("<div class='alert "+m.extra_tags+" alert-dismissible' role='alert' style='margin: 15px 15px 0px -15px;'>"+m.message+"</div>");
    });
}

/// ajax reguest for query search
var frm_srch = $("#query-form"); 
$(frm_srch).submit(function (e) {
    e.preventDefault();
    $.ajax({
        url: frm_srch.attr('action'),
        type: frm_srch.attr('method'),
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: frm_srch.serialize(),
        beforeSend: function() {
            $("#bg-spinner").fadeIn(500);
        },
        complete: function() {
            $("#bg-spinner").fadeOut(500);
        },
        success:function(data){
            $("#content").html(data.rendered_data);
        },
        error:function(data){
            console.log('error')
        },
    });
});

/// ajax request for excel-file search
var frm_file_srch = $("#file-form");
$(frm_file_srch).submit(function (e) {
    e.preventDefault();
    var data = new FormData();
    data.append("excel_file", $("#id_excel_file").get(0).files[0]);
    $.ajax({
        url: frm_file_srch.attr('action'),
        type: frm_file_srch.attr('method'),
        headers:{
            "X-CSRFToken": csrftoken
        },
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        beforeSend: function() {
            $("#bg-spinner").fadeIn(500);
        },
        complete: function() {
            $("#bg-spinner").fadeOut(500);
        },
        success:function(data){
            $("#content").html(data.rendered_data);
        },
        error:function(data){
            console.log('error')
        },
    });
});

/// ajax request for adding devices
var frm = $("#addForm");
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

/// ajax request for deleting devices
$(document).ready(function(){
    $("#delete_id").click(function(){
        if (confirm("Are you sure to delete these items?")){
            var id = [];
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $('#item:checked').each(function(i){
                if ($(this).val() != "on"){
                    console.log($(this).val());
                    id[i]=$(this).val()
                }
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
		            	var get= document.getElementsByName('item');
                        console.log(get);
                        for(var i= 0; i<get.length; i++){
                            console.log('k');
                            get[i].checked= false;}
                        $('#select-all').prop('checked', false);
                        }
                })
            }
        }
    })
})

/// select/deselect all checkboxes
$('#select-all').click(function(event) {   
    if(this.checked) {
        $(':checkbox').each(function() {
            this.checked = true;                        
        });
    } else {
        $(':checkbox').each(function() {
            this.checked = false;                       
        });
    }
}); 