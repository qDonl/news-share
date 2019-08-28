function Banner() {

}

Banner.prototype.createBannerItem = function (banner) {
    // 创建轮播图盒子
    var self = this;
    var tpl = template("banner-item", {"banner": banner});
    var bannerListGroup = $(".banner-list-group");

    var bannerItem = null;
    if (banner) {
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find(".banner-item:last");
    } else {
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find(".banner-item:first");
    }

    self.insertBannerImageEvent(bannerItem);
    self.removeBannerItemEvent(bannerItem);
    self.saveBannerEvent(bannerItem);
};

Banner.prototype.loadBanner = function () {
    var self = this;
    $.get({
        url: '/cms/banner/load/',
        success: function (result) {
            var banners = result['data'];
            for (var i = 0; i < banners.length; i++) {
                var banner = banners[i];
                self.createBannerItem(banner);
            }
        }
    })
};

Banner.prototype.addBannerEvent = function () {
    // 展示添加轮播图盒子
    var self = this;
    var bannerAdd = $("#banner-add");  // 添加轮播图按钮
    bannerAdd.click(function () {
        self.createBannerItem();
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
                        retryCount: 2,
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
    var percent = total.percent.toFixed(0) + '%';

    var bannerListGroup = $(".banner-list-group");
    var bannerItem = bannerListGroup.find(".banner-item:first");
    var bannerBarGoup = bannerItem.find('.banner-process-group');
    var bannerBar = bannerBarGoup.find(".banner-process");
    bannerBarGoup.show();
    bannerBar.css({width: percent});
    bannerBar.text(percent);
};

Banner.prototype.handleFileUploadError = function (err) {
    // 处理上传错误信息
    window.messageBox.showError(err.message);
    console.log('error:' + err + message);
};

Banner.prototype.handleFileUploadComplete = function (resp) {
    // 处理 图片上传完成后的事件
    var bannerListGroup = $(".banner-list-group");
    var bannerItem = bannerListGroup.find(".banner-item:first");
    var bannerBarGoup = bannerItem.find('.banner-process-group');
    var image = bannerItem.find('.thumbnail');

    var domain = "http://pwm9160nr.bkt.clouddn.com/";
    var filename = resp.key;
    var link = domain + filename;

    image.attr({src: link});
    bannerBarGoup.hide();
};

Banner.prototype.saveBannerEvent = function (bannerItem) {
    var saveBtn = bannerItem.find('.banner-save');
    saveBtn.click(function () {
        var image_url = bannerItem.find('.thumbnail').attr('src');
        var priority = bannerItem.find("input[name=priority]").val();
        var link_to = bannerItem.find("input[name=link_to]").val();

        $.post({
            url: "/cms/banner/add/",
            data: {
                image_url: image_url,
                priority: priority,
                link_to: link_to,
            },
            success: function (result) {
                if (result['code'] == 200) {
                    var banner_id = result['data']['banner_id'];
                    console.log('banner ID:' + banner_id);
                    window.messageBox.showSuccess("添加成功");
                } else {
                    window.dataMessage.getMessage(result);
                }
            },
            fail: function (error) {
                window.messageBox.showError(error);
                console.log(error)
            }
        })
    })
};

Banner.prototype.removeBannerItemEvent = function (bannerItem) {
    // 移除轮播图
    var removeBtn = bannerItem.find(".remove-banner");
    var bannerId = bannerItem.attr("data-banner");
    removeBtn.click(function () {
        if (!bannerId) {
            bannerItem.remove();
        }else {
            swalert.alertConfirm({
                "title": "删除",
                'msg': "是否要删除当前轮播图?",
                "confirmCallback": function () {
                    $.get({
                        "url": "/cms/banner/remove/",
                        "data": {
                            bid: bannerId
                        },
                        "success": function (result) {
                            if (result['code']==200) {
                                window.messageBox.showSuccess("删除成功");
                                bannerItem.remove();
                            } else {
                                window.messageBox.showError("发生了错误")
                            }
                        },
                        "fail": function (error) {
                            window.messageBox.showError(error);
                        }
                    })
                }
            })
        }
    })
};

Banner.prototype.run = function () {
    this.addBannerEvent();
    this.loadBanner();
};

$(function () {
    var banner = new Banner();
    banner.run();
});