$(function(){
    var id_changed_field = '#id_site',
        url = '/bid/get-category-by-site/',
        target_select = '#id_categories';

    $(target_select).height('350');

    $(id_changed_field).live('change', function(){
        var self = $(this),
            site_id = self.val()+'/';

        $.getJSON(url+site_id, function(response){
            $(target_select).empty();
            for(var i in response) {
                $(target_select).append('<option value='+response[i].id+'>'+response[i].name+'</option>');
            }
        });
    });
});
