$(function(){
    var class_changed_field = '.field-feature',
        url = '/section/get-parameters-for-feature/';

    $(class_changed_field+' select').live('change', function(){
        var self = $(this),
            feature_id = self.val()+'/',
            target_select = '#'+self.attr('id').replace('-feature', '-parameter');

        $.getJSON(url+feature_id, function(response){
            $(target_select).empty();
            $(target_select).append('<option value="">---------</option>');
            for(var i in response) {
                $(target_select).append('<option value='+response[i].id+'>'+response[i].name+'</option>');
            }
        });
    });
});
