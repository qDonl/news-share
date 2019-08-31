function CMSNewsList() {

}


CMSNewsList.prototype.initPicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,  // 显示 "今日/清除" 按钮
        "format": "yyyy/mm/dd",  // 的定义中文式时间格式
        'startDate': '2019/6/1',  // 起始时间
        'endDate': todayStr,  // 今日为最后时间
        'language': 'zh-CN',  // 语言为 中文
        'todayBtn': 'linked',  // 是否显示"今天"按钮
        'todayHighlight': true,  // 今日日期 高亮显示
        'clearBtn': true,  // 显示 "清除" 按钮
        'autoclose': true,
    };

    startPicker.datepicker(options);
    endPicker.datepicker(options);
};


CMSNewsList.prototype.run = function () {
    this.initPicker();
};

$(function () {
    var cmsNewsPicker = new CMSNewsList();
    cmsNewsPicker.run();
});