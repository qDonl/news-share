function AddStaff() {

}

AddStaff.prototype.addStaffEvent = function () {
    var addBtn = $("#add-btn");
    addBtn.click(function (event) {
        event.preventDefault();
        var group_ids = [];
        var telephone = $("#staff-tel").val();
        $("input[name=group]:checked").each(function (i) {
            group_ids[i] = $(this).val();
        });
        if (!telephone) {
            window.messageBox.showInfo("请输入手机号码");
            return ;
        }
        if (group_ids.length === 0) {
            window.messageBox.showInfo("请选择员工分组");
            return;
        }
        $.post({
            url: '/cms/staff/add/',
            data: {
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

AddStaff.prototype.run = function () {
    this.addStaffEvent();
};

$(function () {
    var addStaff = new AddStaff();
    addStaff.run()
});