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
        _signclick: function(){
            var content = dom.byId("content");
            text  = domAtt.get(content, "value");
            
            request.post("/api/guestbook/"+this.guestbook+"/greeting/", {
                data:{
                    content: text
                },
                headers:{
                    "X-CSRFToken": cookie('csrftoken')
                }
            });
            this._loadgreeting(this.guestbook);
        },
        _switchclick: function(){
            this.guestbook = domAtt.get(dom.byId("txtGuestbook_name"), "value");
            this._loadgreeting(this.guestbook);
        },
        _loadgreeting: function(guestbook){
            dojo.empty(dom.byId("greetingListNode"));
            request("/api/guestbook/"+guestbook+"/greeting/", {
                handleAs: "json"
            }).then(function(data){
                var greetingContainer = dom.byId("greetingListNode");
                arrayUtil.forEach(data.greetings, function(greeting){
                    var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
                });
            });
        },
        postCreate: function(){
            this.inherited(arguments);
            alert(this.guestbook);
            var guestbook = dom.byId("txtGuestbook_name");
            this._loadgreeting(this.guestbook);
            domAtt.set(guestbook, "value", this.guestbook);
            signButton = dom.byId("signButton");
            switchButton = dom.byId("switchButton");
            this.own(
                on(signButton,"click", lang.hitch(this, "_signclick")),
                on(switchButton,"click", lang.hitch(this, "_switchclick"))
            );
        }
    });
});