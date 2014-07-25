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
    var email = $('#email').val();
    var phone = $('#phone').val();
    var password = $('#password').val();
    var repassword = $('#repassword').val();
    if(username==''){
        alert('请填写用户名')
        return false
    }
    if(email==''){
        alert('请填写邮箱')
        return false
    }
    if(password==''){
        alert('请填写密码')
    }
    if(password!=repassword){
        alert('两次密码不一致')
        return false
    }
    $.post('/admin/user/add',
        {
            username : username,
            password : password,
            email   : email,
            phone : phone,
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
    var email = $('#'+identif+'email').val()
    var phone = $('#'+identif+'phone').val()
    var password = $('#'+identif+'password').val()
    var state = $('#'+identif+'state').val()
//    alert(identif)
//    alert(userid+username+password+state)
    if(username==''){
        alert('用户名不能为空')
        return false
    }
    if(email==''){
        alert('邮箱不能为空')
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
            email : email,
            phone : phone,
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
    var title = $('#title').val()
    var category = $('#category').val()
    var article = $('#article').val()
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

function login(){
    var username = $('#username').val()
    var password = $('#password').val()
    if(username==''){
        alert('请输入用户名')
        return false
    }
    if(password==''){
        alert('请输入密码')
        return false
    }
    $.post('/login/',
        {
            username : username,
            password : password
        },
        function(data,status){
            if(data=='admin'){
                alert('hello,admin!')
                location.href='/admin'
            }else if(data=='user'){
                alert('hello,user!')
                location.href='/user/'+username
            }else{
                alert(data)
                location.reload()
            }

        })
    return false
}


function changePassword(obj) {
    alert('aa')
    var state = obj.getAttribute('data-state')
    var username = obj.getAttribute('data-username')
    var oldpassword = $('#oldpassword').val()
    var newpassword = $('#newpassword').val()
    var repassword = $('#repassword').val()
    if(oldpassword==''){
        alert('请输入旧密码')
        return false
    }
    if(newpassword==''){
        alert('请输入新密码')
        return false
    }
    if(repassword!=newpassword){
        alert('两次密码不一致')
        return false
    }
    $.post('/user/changePassword',
        {
            oldpassword : oldpassword,
            newpassword : newpassword,
            repassword : repassword
        },
        function(data,status){
            alert(data)
            if(data=='success'){
                if(state==0){
                     location.href='/admin'
                 }
                else if(state==1){
                     location.href='/user/'+username
                 }
                else{
                    location.href='/login/'
                }
            }
            else{
                location.reload()
            }
        })
}