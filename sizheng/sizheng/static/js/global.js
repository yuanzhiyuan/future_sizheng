/**
 * Created by yuan on 7/17/14.
 */

function passArticle(obj){
    alert(obj.getAttribute('data-articleid'))
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


function addUser(){
    alert('aaa')
    var username = $('#username').val();
    var password = $('#password').val();
    var repassword = $('#repassword').val();
    if(password!=repassword){
        alert('两次密码不一致')
        return false
    }
    $.post('/admin/user/add',
        {
            username : username,
            password : password,
            repassword : repassword
        },
        function(data,status){
            alert(data)
            location.reload()

        })
}

//通过传递obj取得button的属性'data-id'来区分每个用户条目
function updateUser(obj){
//    alert('aaa')
    var identif = obj.getAttribute('data-id')
    var userid = $('#'+identif+'userid').val()
    var username = $('#'+identif+'username').val()
    var password = $('#'+identif+'password').val()
    var state = $('#'+identif+'state').val()
//    alert(identif)
//    alert(userid+username+password+state)
    if(username==''){
        alert('用户名不能为空')
        return false
    }
    if(password==''){
        alert('密码不能为空')
        return false
    }

    $.post('/admin/user/update',
        {
            id : userid,
            username : username,
            password : password,
            state   : state
        },
        function (data, status) {
            alert(data)
            location.reload()
        })
}

function addArticle(){
    var title = $('#title').val()
    var category = $('#category').val()
    var article = $('#article').val()
    if(title==''){
        alert('标题不能为空')
        return false
    }
    if(article==''){
        alert('文章内容不能为空')
        return false
    }
    $.post('/article/add',
        {
            title : title,
            category : category,
            article : article
        },
        function (data, status) {
            alert(data)
            location.reload()
        })
}

function updateArticle(obj){
    alert('aaa')
    var articleid = obj.getAttribute('data-id')
    var title = $('#title')
    var category = $('#category')
    var article = $('#article')
    if(title==''){
        alert('标题不能为空')
        return false
    }
    if(article==''){
        alert('内容不能为空')
        return false
    }
    $.post('/article/update/'+articleid,
        {
            title : title,
            category :category,
            article : article
        },
        function(data,status){
            alert(data)
            location.reload()
        }
    )
}