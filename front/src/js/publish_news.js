function PublishNews() {

}

PublishNews.prototype.initUEditor = function () {
    window.ue = UE.getEditor('ueditor', {
        initialFrameHeight: 400,
        serverUrl: '/ueditor/upload/',
    });
};


PublishNews.prototype.listenUploadEvent = function () {
    // 将文件上传到本地服务器 (已弃用)
    var uploadBtn = $("#thumbnail-btn");
    uploadBtn.change(function () {
        console.log(uploadBtn);
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        $.post({
            url: "/cms/upload/",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                if (data['code'] == 200) {
                    var url = data['data']['url'];
                    var thumbnailFormEle = $("#form-thumbnail");
                    thumbnailFormEle.val(url);
                    thumbnailFormEle.attr({"disabled": true});
                    window.messageBox.showSuccess("添加成功")
                } else {
                    window.dataMessage.getMessage(data)
                }
            },
            fail: function (error) {
                console.log(errro);
            }
        })
    })
};

PublishNews.prototype.qiniuUploadEvent = function () {
    // 文件上传的七牛云服务器
    // https://developer.qiniu.com/kodo/sdk/1283/javascript
    var self = this;
    var uploadBtn = $("#thumbnail-btn");
    uploadBtn.change(function () {
        var file = this.files[0];
        $.get({
            url: '/cms/qntoken/',
            success: function (data) {
                if (data['code'] == 200) {
                    var token = data['token'];
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    console.log("token:" + token + 'key:' + key);

                    var putExtra = {  // 额外参数
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpg', 'image/jpeg'],
                    };
                    var config = {  // 相关配置信息
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z0,
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        'next': self.handleFileUploadNext,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete
                    })
                } else {
                    window.dataMessage.getMessage(data)
                }
            },
            fail: function (error) {
                window.messageBox.showError(error)
            }
        })
    })
};

PublishNews.prototype.handleFileUploadNext = function (response) {
    // 处理上传进度
    var self = this;
    var total = response.total;
    var percent = total.percent.toFixed(0) + '%';  // 不需要小数点
    var progressGroup = $("#progress-group");
    progressGroup.show();
    var progressBar = $(".progress-bar");
    progressBar.css({width: percent});
    progressBar.text(percent);
};

PublishNews.prototype.handleFileUploadError = function (error) {
    // 处理上传图片的错误
    window.messageBox.showError(error.message);
};

PublishNews.prototype.handleFileUploadComplete = function (response) {
    // 接收上传完成后的后端返回信息
    // 返回: key / hash
    var progressGroup = $("#progress-group");
    progressGroup.hide();
    var progressBar = $(".progress-bar");
    progressBar.css({width: 0 + '%'});

    var domain = "http://pwm9160nr.bkt.clouddn.com/";  // 七牛云测试域名
    var filename = response.key;
    var link = domain + filename;

    var thumbnailFormEle = $("#form-thumbnail");
    thumbnailFormEle.val(link);
    thumbnailFormEle.attr({"disabled": true});
    window.messageBox.showSuccess("添加成功");

};


PublishNews.prototype.listenSubmitEvent = function (event) {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name=title]").val();
        var thumbnail = $("input[name=thumbnail]").val();
        var desc = $("input[name=desc]").val();
        var category = $("select[name=category]").val();
        var content = window.ue.getContent();
        $.post({
            url: '/cms/news/publish/',
            data: {
                title: title,
                desc: desc,
                thumbnail: thumbnail,
                category: category,
                content: content
            },
            success: function (data) {
                if (data['code'] == 200) {
                    swalert.alertSuccess("新闻发布成功", function () {
                        window.location.reload();
                    })
                }else{
                    window.dataMessage.getMessage(data);
                }
            },
            fail: function (error) {
                window.messageBox.showError(error)
            }
        })
    })

};

PublishNews.prototype.run = function () {
    this.qiniuUploadEvent();
    this.initUEditor();
    this.listenSubmitEvent();
};

$(function () {
    var publishNews = new PublishNews();
    publishNews.run();
});