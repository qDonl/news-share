// 面向对象
// 1. 添加属性
// 通过this关键字，绑定属性，并且指定他的值。
// 原型链
// 2. 添加方法
// 在Banner.prototype上绑定方法就可以了。

// function Banner() {
//     // 这个里面写的代码
//     // 相当于是Python中的__init__方法的代码
//
// Banner.prototype.greet = function (word) {
//     console.log('hello ',word);
// };
//
// var banner = new Banner();
// console.log(banner.person);
// banner.greet('hello world');

function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $("#banner-group");
    this.index = 1;
    this.leftArrow = $(".left-arrow");
    this.rightArrow = $(".right-arrow");
    this.bannerUl = $("#banner-ul");
    this.liList = this.bannerUl.children("li");
    this.bannerCount = this.liList.length;
    this.pageControl = $(".page-control");
}

Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone();
    self.bannerUl.append(firstBanner);
    self.bannerUl.prepend(lastBanner);
    self.bannerUl.css({"width": self.bannerWidth * (self.bannerCount + 2), 'left': -self.bannerWidth});
};

Banner.prototype.initPageControl = function () {
    var self = this;
    for (var i = 0; i < self.bannerCount; i++) {
        var circle = $("<li></li>");
        self.pageControl.append(circle);
        if (i === 0) {
            circle.addClass("active");
        }
    }
    self.pageControl.css({"width": self.bannerCount * 12 + 8 * 2 + 16 * (self.bannerCount - 1)});
};

Banner.prototype.toggleArrow = function (isShow) {
    var self = this;
    if (isShow) {
        self.leftArrow.show();
        self.rightArrow.show();
    } else {
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

Banner.prototype.animate = function () {
    var self = this;
    self.bannerUl.animate({"left": -798 * self.index}, 500);
    var index = self.index;
    if (index === 0) {
        index = self.bannerCount - 1;
    } else if (index === self.bannerCount + 1) {
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pageControl.children('li').eq(index).addClass("active").siblings().removeClass('active');
};

Banner.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1) {
            self.bannerUl.css({"left": -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    }, 2000);
};


Banner.prototype.listenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if (self.index === 0) {
            // ==：1 == '1'：true
            // ==== 1 != '1'
            self.bannerUl.css({"left": -self.bannerCount * self.bannerWidth});
            self.index = self.bannerCount - 1;
        } else {
            self.index--;
        }
        self.animate();
    });

    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({"left": -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    });
};

Banner.prototype.listenBannerHover = function () {
    var self = this;
    this.bannerGroup.hover(function () {
        // 第一个函数是，把鼠标移动到banner上会执行的函数
        clearInterval(self.timer);
        self.toggleArrow(true);
    }, function () {
        // 第二个函数是，把鼠标从banner上移走会执行的函数
        self.loop();
        self.toggleArrow(false);
    });
};

Banner.prototype.listenPageControl = function () {
    var self = this;
    self.pageControl.children("li").each(function (index, obj) {
        $(obj).click(function () {
            self.index = index;
            self.animate();
        });
    });
};

Banner.prototype.run = function () {
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenBannerHover();
    this.listenArrowClick();
    this.listenPageControl();
};


// 首页新闻加载
function News() {
    this.page = 2;  // 当前获取的是 "第几页"
    this.category_id = 0;
    this.loadMoreBtn = $("#load-more");

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

News.prototype.listenLoadMoreEvent = function () {
    // ajax 加载更多新闻
    var self = this;
    self.loadMoreBtn.click(function (event) {
        event.preventDefault();
        $.get({
            url: '/news/list/',
            data: {
                p: self.page,
                category_id: self.category_id,
            },
            success: function (data) {
                if (data['code'] == 200) {
                    var newses = data['data'];
                    if (newses.length > 0) {
                        var tpl = template("news-item", {"newses": newses});
                        var ul = $(".list-inner-group");
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        self.loadMoreBtn.hide();
                    }

                } else {
                    window.dataMessage.getMessage(data)
                }
            },
            fail: function (error) {
                console.log(error)
            }
        })
    });
};

News.prototype.listenCategorySwitchEvent = function () {
    var self = this;
    var listTab = $(".list-tab");
    listTab.children().click(function () {
        var li = $(this);
        var category_id = li.attr("data-category");
        var page = 1;
        self.loadMoreBtn.show();
        $.get({
            url: '/news/list/',
            data: {
                category_id: category_id,
                p: page
            },
            success: function (data) {
                if (data['code'] == 200) {
                    var newses = data['data'];
                    var tpl = template("news-item", {"newses": newses});
                    var ul = $(".list-inner-group");
                    ul.empty();
                    ul.append(tpl);
                    self.page = 2;
                    self.category_id = category_id;
                    li.addClass('active').siblings().removeClass('active');
                } else {
                    window.dataMessage.getMessage(data)
                }
            }
        })
    });
};

News.prototype.run = function () {
    this.listenLoadMoreEvent();
    this.listenCategorySwitchEvent();
};

$(function () {
    var banner = new Banner();
    banner.run();

    var news = new News();
    news.run();
});