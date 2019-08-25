// 点击登录按钮，弹出模态对话框
$(function () {
    $("#btn").click(function () {
        $(".mask-wrapper").show();
    });

    $(".close-btn").click(function () {
        $(".mask-wrapper").hide();
    });
});

function Auth() {
    var self = this;
    self.markWrapper = $(".mask-wrapper");
    self.scrollWrapper = $(".scroll-wrapper");
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
    var self = this;
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
                    var messageObj = result['msg'];
                    if (typeof messageObj == "string" || messageObj.constructor == String) {
                        window.messageBox.showError(messageObj)
                    } else {
                        for (var key in messageObj) {
                            var messages = messageObj[key];
                            var message = messages[0];
                            window.messageBox.showError(message);
                        }
                    }
                }
            },
            'fail': function (error) {
                window.messageBox("出现了点小毛病, 重新试一试 ~")
            }
        })
    })


};

Auth.prototype.run = function () {
    this.listenShowHideEvent();
    this.listenSwitch();
    this.listenSignin();
};


$(function () {
    var auth = new Auth();
    auth.run();
});