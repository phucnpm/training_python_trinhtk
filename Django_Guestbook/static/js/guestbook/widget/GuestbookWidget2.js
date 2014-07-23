
define([
    "dojo/_base/declare",
    "dijit/form/Button",
    "dijit/layout/ContentPane",
    "dijit/form/SimpleTextarea",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dojo/dom",
    "dojo/cookie",
    "dojo/request",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare,
            Button,
            ContentPane,
            Content,
            _WidgetBase,
            _TemplatedMixin,
            dom,
            cookie,
            request,
            template){
    var guestbookContainer = new ContentPane({
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
                        "X-CSRFToken": cookie('csrftoken')
                    }
                });
                location.reload();
            }
        },"signButton").startup();
    var content = new Content({
            name: "content",
            rows: "4",
            cols: "50",
            style: "width:auto;",
            id: "content"
        });
        guestbookContainer.addChild(content);
        guestbookContainer.addChild(signButton);
        guestbookContainer.startup();
    return declare([_WidgetBase, _TemplatedMixin, guestbookContainer, content, signButton], {
        guestbookContainer : guestbookContainer,
        baseClass: "GuestbookWidget",
        templateString : template
    });

});