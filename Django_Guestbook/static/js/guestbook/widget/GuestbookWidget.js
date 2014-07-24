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
    "dojo/request/notify",
    "dojo/parser",
    "dojo/ready",
    "dojo/cookie",
    "dojo/dom-attr",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare, baseFx, lang, mouse, on, _WidgetBase, arrayUtil, GreetingWidget, _TemplatedMixin,
            dom, request, notify, parser, ready, cookie, domAtt, template){
    return declare("app.FirstWidget",[_WidgetBase, _TemplatedMixin], {
        guestbook : "default_guestbook",
        templateString: template,
        baseClass: "GuestbookWidget",
        mouseAnim: null,
        baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",
        _signclick: function(evt){
            var content = dom.byId("content");
            text  = domAtt.get(content, "value");
            evt.stopPropagation();
            evt.preventDefault();
            request.post("/api/guestbook/"+this.guestbook+"/greeting/", {
                data:{
                    content: text
                },
                headers:{
                    "X-CSRFToken": cookie('csrftoken')
                },
                timeout : 1000
            });
            content = dom.byId("content");
            domAtt.set(content, "value", "");
            this._loadgreeting(this.guestbook, 500);
        },
        _switchclick: function(){
            this.guestbook = domAtt.get(dom.byId("txtGuestbook_name"), "value");
            this._loadgreeting(this.guestbook, 0);
        },
        _loadgreeting: function(guestbook, time){
            var start = new Date().getTime();
            while (new Date().getTime() < start + time);
            dojo.empty(dom.byId("greetingListNode"));
            request("/api/guestbook/"+guestbook+"/greeting/", {
                handleAs: "json"
            }).then(function(data){
                var greetingContainer = dom.byId("greetingListNode");
                var newDocFrag = document.createDocumentFragment();
                var count = 0;
                arrayUtil.forEach(data.greetings, function(greeting){
                    var widget = new GreetingWidget(greeting).placeAt(newDocFrag);
                });
                greetingContainer.appendChild(newDocFrag);
            });
        },
        postCreate: function(){
            this.inherited(arguments);
            var guestbook = dom.byId("txtGuestbook_name");
            this._loadgreeting(this.guestbook, 0);
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