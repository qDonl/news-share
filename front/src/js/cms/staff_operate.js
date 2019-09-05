function StaffOperate() {

}

StaffOperate.prototype.addStaffEvent = function () {
    var addBtn = $("#add-btn");
    var telReadonly = $("#staff-tel").val();
    addBtn.click(function (event) {
        event.preventDefault();
        var group_ids = [];
        var telephone = $("#staff-tel").val();
        $("input[name=group]:checked").each(function (i) {
            group_ids[i] = $(this).val();
        });
        if (!telephone) {
            window.messageBox.showInfo("请输入手机号码");
            return;
        }
        if (group_ids.length === 0) {
            window.messageBox.showInfo("请选择员工分组");
            return;
        }
        var url = '';
        if(!telReadonly){
            url = '/cms/staff/add/';
        }else {
            url = '/cms/staff/update/';
        }
        $.post({
            'url': url,
            "data": {
                "telephone": telephone,
                "group": group_ids,
            },
            success: function (result) {
                if (result['code'] == 200) {
                    window.location = '/cms/staff/';
                } else {
                    window.dataMessage.getMessage(result);
                }
            },
            fail: function (error) {
                console.log(error)
            }
        })
    })
};

StaffOperate.prototype.removeStaffEvent = function () {
    var removeBtn = $(".remove-staff");
    removeBtn.click(function (event) {
        event.preventDefault();
        var item = $(this);
        swalert.alertConfirm({
            title: "移除",
            msg: "请再次确定要移除此员工",
            confirmCallback: function () {
                var uid = item.attr('data-id');
                console.log(uid);
                $.get({
                    url: '/cms/staff/remove/',
                    data: {
                        uid: uid
                    },
                    success: function (result) {
                        if (result['code'] == 200) {
                            window.location.reload();
                        } else {
                            window.dataMessage.getMessage(result)
                        }
                    },
                    fail: function (error) {
                        console.log(error)
                    }
                })
            }
        });
    })
};

StaffOperate.prototype.run = function () {
    this.addStaffEvent();
    this.removeStaffEvent();
};

$(function () {
    var staffOperate = new StaffOperate();
    staffOperate.run()
});