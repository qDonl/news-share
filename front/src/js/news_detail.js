function NewsDetail() {

}

NewsDetail.prototype.publishCommentEvent = function () {
    var submitBtn = $(".comment-submit-btn");
    var textarea = $("textarea[name=comment]");
    submitBtn.click(function (event) {
        event.preventDefault();

        var news_id = submitBtn.attr('data-news');
        var content = textarea.val();
        $.post({
            url: '/news/comment/',
            data: {
                news_id: news_id,
                content: content,
            },
            success: function (result) {
                if (result['code'] == 200) {
                    var comment = result['data'];
                    var tpl = template("comment-item", {"comment": comment});
                    var commentGroup = $(".comment-list");
                    commentGroup.prepend(tpl);
                    textarea.val('');
                }else {
                    window.dataMessage.getMessage(result)
                }
            },
            fail: function (error) {
                window.messageBox.showError(error)
            }
        })
    })
};

NewsDetail.prototype.run = function () {
    this.publishCommentEvent();
};

$(function () {
    var newsDetail = new NewsDetail();
    newsDetail.run();
});