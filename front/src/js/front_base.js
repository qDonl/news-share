// 处理登录后 用户退出显示
function FrontBase() {

}

FrontBase.prototype.listenAuthBoxHover = function () {
    var authBox = $(".auth-box");
    var userMoreBox = $(".user-more-box");

    authBox.hover(function () {
        userMoreBox.show();
    }, function () {
        userMoreBox.hide();
    })
};

FrontBase.prototype.listenImgCaptchaEvent = function () {
    var imgCaptcha = $(".img-captcha");
    var imgSrc = imgCaptcha.attr('src');
    imgCaptcha.click(function () {
        console.log(imgSrc);
        var newImgSrc = imgSrc + "?change=" + Math.random();
        imgCaptcha.attr({"src": newImgSrc});
    });

};

FrontBase.prototype.run = function () {
    this.listenAuthBoxHover();
    this.listenImgCaptchaEvent();
};

$(function () {
    var frontBase = new FrontBase();
    frontBase.run();
});


// -----------
// 模态框控制
$(function () {
    $("#btn").click(function () {
        $(".mask-wrapper").show();
    });

    $(".close-btn").click(function () {
        $(".mask-wrapper").hide();
    });
});

// 用户 注册/登录
function Auth() {
    var self = this;
    self.markWrapper = $(".mask-wrapper");
    self.scrollWrapper = $(".scroll-wrapper");
    self.smsCaptchaBtn = $(".sms-captcha-btn");
}

Auth.prototype.showEvent = function () {
    // 显示模态框
    this.markWrapper.show();
};

Auth.prototype.hideEvent = function () {
    // 隐藏模态框
    this.markWrapper.hide();
};

Auth.prototype.listenShowHideEvent = function () {
    // 监听登录注册模态框显示隐藏
    var self = this;
    var signinBtn = $(".signin-btn");
    var signupBtn = $(".signup-btn");
    var closeBtn = $(".close-btn");
    var scrollWrapper = $(".scroll-wrapper");

    signinBtn.click(function () {
        self.showEvent();
        scrollWrapper.css({"left": 0});
    });

    signupBtn.click(function () {
        self.showEvent();
        scrollWrapper.css({"left": -400});
    });

    closeBtn.click(function () {
        self.hideEvent();
    })
};

Auth.prototype.listenSwitch = function () {
    // 监听登录注册模态框切换
    var self = this;
    $(".switch").click(function () {
        var currentLeft = self.scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);
        if (currentLeft < 0) {
            self.scrollWrapper.animate({"left": '0'});
        } else {
            self.scrollWrapper.animate({"left": "-400px"});
        }
    });
};

Auth.prototype.listenSignin = function () {
    // 登录
    var signGroup = $(".signin-group");
    var telephoneInput = signGroup.find("input[name='telephone']");
    var passwordInput = signGroup.find("input[name='password']");
    var rememberChecked = signGroup.find("input[name='remember']");

    var submitBtn = signGroup.find('.submit-btn');

    submitBtn.click(function () {
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberChecked.prop('checked');

        $.post({
            'url': '/account/login/',
            'data': {
                telephone: telephone,
                password: password,
                remember: remember ? 1 : 0,
            },
            'success': function (result) {
                // 登录消息提示
                if (result['code'] == 200) {
                    window.location.reload();
                } else {
                    window.dataMessage.getMessage(result);
                }
            },
            'fail': function (error) {
                window.messageBox("出现了点小毛病, 重新试一试 ~")
            }
        })
    })
};

Auth.prototype.smsSuccessEvent = function () {
    // 手机验证法发送成功, 用于解绑 click 事件
    var self = this;

    window.messageBox.showSuccess("发送成功");
    var count = 3;
    var timer = setInterval(function () {  // 倒计时中, 无法使用 click事件
        self.smsCaptchaBtn.unbind('click');  // unbind 取消自身的点击事件
        count--;
        self.smsCaptchaBtn.addClass('disabled');
        self.smsCaptchaBtn.text(count + ' s');
        if (count <= 0) {
            self.smsCaptchaBtn.removeClass('disabled');
            self.smsCaptchaBtn.text('发送验证码');
            clearInterval(timer);
            self.listenSMSCaptchaEvent();  // 可以重新使用 click
        }
    }, 1000)
};

Auth.prototype.listenSMSCaptchaEvent = function () {
    // 监听发送手机验证码 -- click 事件
    var self = this;
    var telephoneInput = $(".signup-group input[name=telephone]");

    self.smsCaptchaBtn.click(function () {
        var telephone = telephoneInput.val();
        if (!telephone) {
            window.messageBox.showError("请输入手机号码");
            return
        } else if (!(/^1[34578]\d{9}$/.test(telephone))) {
            window.messageBox.showError('请输入正确格式的手机号码');
            return
        }

        $.get({
            url: '/account/sms_captcha/',
            data: {
                telephone: telephone,
            },
            success: function (data) {
                if (data['code'] == 200) {
                    self.smsSuccessEvent();
                } else {
                    window.messageBox.showError(data['msg'])
                }
            },
            fail: function (error) {
                window.messageBox.showError(error)
            }
        })
    });
};

Auth.prototype.listenRegisterEvent = function () {
    // 用户注册
    var signupGroup = $(".signup-group");
    var submitBtn = signupGroup.find(".submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var telephoneEle = signupGroup.find("input[name=telephone]");
        var smsCaptchaEle = signupGroup.find("input[name=sms_captcha]");
        var imgCaptchaEle = signupGroup.find("input[name=img_captcha]");
        var usernameEle = signupGroup.find("input[name=username]");
        var password1Ele = signupGroup.find("input[name=password1]");
        var password2Ele = signupGroup.find("input[name=password2]");

        var telephone = telephoneEle.val();
        var smsCaptcha = smsCaptchaEle.val();
        var username = usernameEle.val();
        var password1 = password1Ele.val();
        var password2 = password2Ele.val();
        var imgCaptcha = imgCaptchaEle.val();

        $.post({
            url: '/account/register/',
            data: {
                telephone: telephone,
                sms_captcha: smsCaptcha,
                username: username,
                password1: password1,
                password2: password2,
                img_captcha: imgCaptcha,
            },
            success: function (data) {
                if (data['code'] == 200) {
                    window.location.reload();
                } else {
                    window.dataMessage.getMessage(data);
                }
            },
            fail: function (error) {
                window.messageBox.showError("出了点小毛病")
            }
        })
    });


};

Auth.prototype.run = function () {
    this.listenShowHideEvent();
    this.listenSwitch();
    this.listenSignin();
    this.listenSMSCaptchaEvent();
    this.listenRegisterEvent();
};


$(function () {
    var auth = new Auth();
    auth.run();
});


$(function () {
    if (template) {
        // 定义 art-template 模板过滤器
        template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);
            var dateStamp = date.getTime();
            var nowStamp = (new Date()).getTime();
            var timeStamp = (nowStamp - dateStamp) / 1000;

            if (timeStamp < 60) {  // 一分钟之内
                return "刚刚"
            } else if (timeStamp >= 60 && timeStamp < (60 * 60)) {  // 1分钟 ~ 1小时间
                var minutes = parseInt(timeStamp / 60);
                return minutes + "分钟前"
            } else if (timeStamp >= 60 * 60 && timeStamp < (60 * 60 * 24)) {  // 1小时 ~ 1天间
                var hours = parseInt(timeStamp / (60 * 60));
                return hours + "小时前"
            } else if (timeStamp >= 60 * 60 * 24 && timeStamp < (60 * 60 * 24 * 30)) {  // 1天 ~ 1月
                var days = parseInt(timeStamp / (60 * 60 * 24));
                return days + "天前";
            } else {
                var year = date.getFullYear();
                var month = date.getMonth();
                var day = date.getDate();
                var hour = date.getDay();
                var minute = date.getMinutes();
                return year + "/" + month + "/" + day + " " + hour + ":" + minute;
            }
        }
    }
});