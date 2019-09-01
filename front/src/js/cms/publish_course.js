function PublishCourse() {

}

PublishCourse.prototype.initUEditor = function (){
    window.vUe = UE.getEditor("video-desc", {
        serverUrl: "/ueditor/upload/",
        initialFrameHeight: 400,
    })
};

PublishCourse.prototype.submitCourseInfoEvent = function () {
    var submitBtn = $("#submit-course");
    submitBtn.click(function () {
        var title = $("input[name=title]").val();
        var category = $("select[name=category]").val();
        var teacher = $("select[name=teacher]").val();
        var video = $("input[name=video]").val();
        var cover = $("input[name=cover]").val();
        var price = $("input[name=price]").val();
        var duration = $("input[name=duration]").val();
        var desc = window.vUe.getContent();
        console.log(title, category, teacher, video, cover, price, duration, desc);

        $.post({
            url: "/cms/course/publish/",
            data: {
                name: title,
                category_id: category,
                teacher_id: teacher,
                video_link: video,
                cover_link: cover,
                price: price,
                duration: duration,
                desc: desc,
            },
            success: function (result) {
                console.log(result);
                if (result['code'] == 200) {
                    swalert.alertConfirm({
                        title: "Success",
                        msg: "发布成功",
                        confirmCallback: function () {
                            window.location.reload();
                        }
                    })
                }else {
                    window.dataMessage.getMessage(result)
                }
            },
            fail: function (error) {
                window.messageBox.showError(error);
                console.log(error)
            }
        })
    })
};

PublishCourse.prototype.run = function () {
    this.initUEditor();
    this.submitCourseInfoEvent();
};

$(function () {
    var publishCourse = new PublishCourse();
    publishCourse.run();
});