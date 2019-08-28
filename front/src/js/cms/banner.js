function Banner() {

}


Banner.prototype.addBannerEvent = function () {
    // 展示添加轮播图盒子
    var self = this;
    var bannerAdd = $("#banner-add");
    var bannerListGroup = $(".banner-list-group");
    bannerAdd.click(function () {
        var tpl = template("banner-item");
        bannerListGroup.prepend(tpl);

        var bannerItem = bannerListGroup.find(".banner-item:first");
        bannerItem.click(function () {
            self.insertBannerImageEvent(bannerItem);
        })
    })
};

Banner.prototype.insertBannerImageEvent = function (bannerItem) {
    // 插入轮播图图片
    var self = this;
    var image = bannerItem.find(".thumbnail");
    var imgInput = image.siblings(".image-input");
    image.click(function () {
        imgInput.click();
    });

    imgInput.change(function () {
        var file = this.files[0];
        console.log('file:' + file);
        $.get({
            url: "/cms/qntoken/",
            success: function (result) {
                if (result['code'] == 200) {
                    var token = result['token'];
                    console.log('token:' + token);
                    var key = "banner" + (new Date()).getTime() + "." + file.name.split('.')[1];

                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpg', 'image/jpeg'],
                    };

                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z0,
                    };

                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        'next': self.handleFileUploadProcess,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete,
                    });
                } else {
                    window.dataMessage.get(result);
                }
            },
            fail: function (error) {
                window.messageBox.showError(error);
            }
        })
    })
};
Banner.prototype.handleFileUploadProcess = function (resp) {
    var total = resp.total;
    var percent = total.percent;
    console.log(percent);
};

Banner.prototype.handleFileUploadError = function (err) {
    window.messageBox.showError(err.message);
    console.log('error:' + err + message);
};


Banner.prototype.handleFileUploadComplete = function (resp) {
    var image = $('.thumbnail');

    var domain = "http://pwm9160nr.bkt.clouddn.com/";
    var filename = resp.key;
    var link = domain + filename;

    image.attr({src: link});

};

Banner.prototype.run = function () {
    this.addBannerEvent();
};

$(function () {
    var banner = new Banner();
    banner.run();
});