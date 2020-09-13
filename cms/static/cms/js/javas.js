$('.like').on('click',function(){
    if ($(this).text() == 'favorite')
    {
        $(this).text('favorite-border');
        $(this).addClass('black-text').removeClass('red-text')
    }
    else{
         $(this).text('favorite');
          $(this).addClass('red-text').removeClass('black-text');

    }
    $.post({
        url:'{% url "app-cms:like"  %}',
        header:{'X-CSRFToken':'{{csrf-token}}'},
        data:{
            id:$(this).data('id'),
            type:$(this).data('type')
        },
        success:function (data) {
            if (data['message'])
            {
                M.toast({html:'<i class="material-icons yellow-text">warning</i>'+data['message']});
            }
            else
            {
                 M.toast({html:'<i class="material-icons yellow-text">warning</i> لطفا براي نظر دادن وارد سايت شويد'});
            }

        },
        error:function (a,b,c,d) {

                  M.toast({html:'<i class="material-icons red-text">warning</i>يه مشكلي پيش اومده'});
        }
    });
});