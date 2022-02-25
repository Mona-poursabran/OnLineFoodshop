$('.delete').on('click', function(event){
    event.preventDefault();
    var $this = $(this)
    if(confirm('Are you sure?')){
        $.ajax({
            url : $this.attr("href"),
            type : "GET",
            datatype: "json",

            success : function(resp){
                if(resp.message === 'success'){
                    $this.parents('.record').remove()
                    window.location.replace(URL); 
                }
            },
            error:function(resp){
                console.log('Sth went wrong!')
            }
        })
    }
})