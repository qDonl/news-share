function CourseDetail() {

}

CourseDetail.prototype.initialPlayerContainer = function () {
    var spanInfo = $("#video-info");
    var videourl = spanInfo.attr('data-video');
    var cover = spanInfo.attr('data-cover');
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: videourl,
        image: cover,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        tokenEncrypt: true,
        ak: '07d23be584da44ff87f41952fed4fecd'
    });
    player.on('beforePlay', function (e) {
        if (!/m3u8/.test(e.file)) {
            return;
        }
        $.get({
            // 获取token的url
            'url': '/course/token/',
            'data': {
                'video': videourl
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    player.setToken(e.file, token);
                } else {
                    window.messageBox.showError("token错误")
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
};


CourseDetail.prototype.run = function () {
    this.initialPlayerContainer();
};

$(function () {
    var courseDetail = new CourseDetail();
    courseDetail.run();
});
