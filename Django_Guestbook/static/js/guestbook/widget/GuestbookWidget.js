
function getCookie(name) {
    var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
}
define([
    "dojo/_base/declare",
    "dijit/form/Button",
    "dijit/layout/ContentPane",
    "dijit/form/SimpleTextarea",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dojo/dom",
    "dojo/request"
], function(declare,
            Button,
            ContentPane,
            Content,
            _WidgetBase,
            _TemplatedMixin,
            dom,
            request){
    var greetingContainer = new ContentPane({
        title: "Greetings",
        content: "Content:",
        id: "guestbook"
    },"guestbook");
    var signButton = new Button({
        value: "Sign Guestbook",
        id: "signButton",
        onClick: function(){
            var content = dom.byId("content");
            text  = dojo.getAttr(content, "value");
            urllength = window.location.toString().split('/').length
            guestbook_name = window.location.toString().split('/')[urllength-1]
            request.post("/api/guestbook/"+guestbook_name+"/greeting/", {

                data:{
                    content: text
                },
                headers:{
                    "X-CSRFToken": getCookie('csrftoken')
                }
            });
            location.reload();
        }
    });
    var content = new Content({
        name: "content",
        rows: "4",
        cols: "50",
        style: "width:auto;",
        id: "content"
    });
    greetingContainer.addChild(content);
    greetingContainer.addChild(signButton);
    greetingContainer.startup();
});