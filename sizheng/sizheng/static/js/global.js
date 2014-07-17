/**
 * Created by yuan on 7/17/14.
 */

function passArticle(obj){
    $.post('/admin/article/verify',
        {
            articleid : obj.getAttribute('data-articleid'),
            type      : 'pass'
        },
        function(data,status){
            alert(data)
            location.reload()
        })
}


function unpassArticle(obj){
    $.post('/admin/article/verify',
        {
            articleid : obj.getAttribute('data-articleid'),
            type      : 'unpass'
        },
        function(data,status){
            alert(data)
            location.reload()
        })
}
function deleteArticle(obj){
    $.post('/admin/article/delete',
        {
            articleid : obj.getAttribute('data-articleid')

        },
        function(data,status){
            alert(data)
            location.reload()
        })

}