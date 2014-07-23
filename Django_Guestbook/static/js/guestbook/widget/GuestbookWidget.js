define([
    "dojo/_base/declare",
    "dojo/_base/fx",
    "dojo/_base/lang",
    "dojo/mouse",
    "dojo/on",
    "dijit/_WidgetBase",
    "dojo/_base/array",
    "guestbook/widget/GreetingWidget",
    "dijit/_TemplatedMixin",
    "dojo/dom",
    "dojo/request",
    "dojo/parser",
    "dojo/ready",
    "dojo/cookie",
    "dojo/dom-attr",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare, baseFx, lang, mouse, on, _WidgetBase, arrayUtil, GreetingWidget, _TemplatedMixin,
            dom, request, parser, ready, cookie, domAtt, template){
    return declare("app.FirstWidget",[_WidgetBase, _TemplatedMixin], {
        guestbook : "default_guestbook",
        templateString: template,
        baseClass: "GuestbookWidget",
        mouseAnim: null,
        baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",
        _signclick: function(guestbook){
            var content = dom.byId("content");
            text  = domAtt.get(content, "value");

            request.post("/api/guestbook/"+guestbook+"/greeting/", {
                data:{
                    content: text
                },
                headers:{
                    "X-CSRFToken": cookie('csrftoken')
                }
            });

            location.reload();
        },
        _switchclick: function(){
            var guestbook = dom.byId("guestbook_name");
            guestbook_name = domAtt.get(guestbook, "value");
            window.location.replace(url);
        },
        postCreate: function(){
            this.inherited(arguments);
//            alert(this.guestbook);
            var guestbook = dom.byId("guestbook_name");
            domAtt.set(guestbook, "value", this.guestbook);
            request("/api/guestbook/"+this.guestbook+"/greeting/", {
                handleAs: "json"
            }).then(function(data){
                var greetingContainer = dom.byId("greetingListNode");
                arrayUtil.forEach(data.greetings, function(greeting){
                    var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
                });
            });
            signButton = dom.byId("signButton");
            switchButton = dom.byId("switchButton");
            this.own(
                on(signButton,"click", lang.hitch(this, "_signclick", this.guestbook)),
                on(switchButton,"click", lang.hitch(this, "_switchclick"))
            );
        }
    });
});