function NewsCategory() {

}

NewsCategory.prototype.listenAddCategoryEvent = function () {
    var addBtn = $("#add-btn");
    var categoryTable = $("#category-table");
    addBtn.click(function () {
        swalert.alertOneInput({
            "title": "添加分类",
            "placeholder": "请输入新分类",
            "confirmCallback": function (inputVal) {
                $.post({
                    url: "/cms/news/category/add/",
                    data: {
                        name: inputVal,
                    },
                    success: function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            swalert.close();
                            window.dataMessage.getMessage(data);
                        }

                    },
                    fail: function (error) {
                        swalert.close();
                        console.log('===========');
                        console.log(error);
                        console.log('===========');
                    }
                })
            }
        })
    })
};

NewsCategory.prototype.listenEditCategoryEvent = function () {
    var editBtn = $(".edit-btn");
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        swalert.alertOneInput({
            title: "修改新闻分类",
            placeholder: name,
            confirmCallback: function (inputVal) {
                $.post({
                    url: "/cms/news/category/edit/",
                    data: {
                        pk: pk,
                        name: inputVal,
                    },
                    success: function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            window.dataMessage.getMessage(data)
                        }
                    },
                    fail: function (error) {
                        window.messageBox.showError("发生错误, 请重新尝试");
                    }
                })
            }
        });

    })
};

NewsCategory.prototype.listenDeleteCategoryEvent = function () {
    var deleteBtn = $(".delete-btn");
    deleteBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        swalert.alertConfirm({
            title: "删除新闻分类",
            msg: "你想要删除这条新闻分类吗?",
            confirmCallback: function () {
                $.post({
                    url: "/cms/news/category/delete/",
                    data: {
                        pk: pk,
                    },
                    success: function (data) {
                        if (data['code'] == 200){
                            window.location.reload();
                        }else {
                            window.dataMessage.getMessage(data);
                        }
                    },
                    fail: function (error) {
                        window.messageBox.showError('发生了错误');
                    }
                })
            }
        })
    })
};


NewsCategory.prototype.run = function () {
    this.listenAddCategoryEvent();
    this.listenEditCategoryEvent();
    this.listenDeleteCategoryEvent();
};


$(function () {
    var newCategory = new NewsCategory();
    newCategory.run();
});