$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});








function DataMessage() {

}

DataMessage.prototype.getMessage = function (result) {
    // 顶部消息提示集成到 window 中
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
};

window.dataMessage = new DataMessage();