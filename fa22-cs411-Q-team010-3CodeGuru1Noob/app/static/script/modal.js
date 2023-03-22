$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'New Task') {
            console.log('Error');
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            console.log('edit');
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#submit-task').click(function () {
        const title =document.getElementById('submit-title').value;
        const cookmin =document.getElementById('submit-cookmin').value;
        console.log(title)
        console.log(cookmin)
        var t = {
  "title":title,
  "cookmin":cookmin
  }
        console.log($('#task-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: '/create',
            data:JSON.stringify(t), //将对象转为为json字符串
      dataType:"json",
      contentType:"application/json", //这个必须，不然后台接受时会出现乱码现象
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });





    $('#update-pwd').click(function () {
        const username =document.getElementById('submit-username').value;
        const password =document.getElementById('submit-password').value;
        console.log(username)
        console.log(password)
        var t = {
		"userName":username,
		"passWord":password
	 }
        console.log($('#task-modal').find('.form-control').val())
        $.ajax({
            type: 'POST',
            url: '/editUser',
            data:JSON.stringify(t), //将对象转为为json字符串
		    dataType:"json",
		    contentType:"application/json", //这个必须，不然后台接受时会出现乱码现象
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    $('.remove').click(function () {
        const remove = $(this)
        console.log(remove.data('source'))
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            // url:  '/delete/20',
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
    $('#submit-recipe').click(function () {
        const tID = document.getElementById('keyword').value //$('#recipe-form-display').attr('taskID');
        console.log(tID) //$('#recipe-modal').find('.form-control').val()
        $.ajax({
            type: 'POST',
            // url: '/search/' + tID,
            url: '/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description': $('#recipe-modal').find('.form-control').val()
            }),
            success: function (res) {
                console.log(res.response);
                $("html").html(res);
            },
            error: function () {
                console.log('Error');
            }
        });
    });



});

