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
    "dojo/dom-construct",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare, baseFx, lang, mouse, on, _WidgetBase, arrayUtil, GreetingWidget, _TemplatedMixin,
            dom, request, notify, parser, ready, cookie, domAtt, domConstruct, template){
    return declare("app.FirstWidget",[_WidgetBase, _TemplatedMixin], {
        guestbook : "default_guestbook",
        templateString: template,
        baseClass: "GuestbookWidget",
        mouseAnim: null,
        baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",

        _signclick: function(evt){
            text = this.contentNode.value;
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
            this.contentNode.value = "";
            this._loadgreeting(this.guestbook, 500);
        },

        _switchclick: function(){
            this.guestbook = this.guestbookNode.value;
            this._loadgreeting(this.guestbook, 0);
        },

        _loadgreeting: function(guestbook, time){
            var start = new Date().getTime();
            while (new Date().getTime() < start + time);
            this.greetingListNode.innerHTML = "";

            request("/api/guestbook/"+guestbook+"/greeting/", {
                handleAs: "json"
            }).then(function(data){
                var greetingContainer = this.greetingListNode;
                var newDocFrag = document.createDocumentFragment();
                var count = 0;
                arrayUtil.forEach(data.greetings, function(greeting){
                    var widget = new GreetingWidget(greeting).placeAt(newDocFrag);
                });
//                greetingContainer.appendChild(newDocFrag);
                domConstruct.place(newDocFrag, greetingContainer);

            });
        },

        postCreate: function(){
            this.inherited(arguments);
            this._loadgreeting(this.guestbook, 0);
            this.guestbookNode.value = this.guestbook;
            this.own(
                on(this.signButtonNode,"click", lang.hitch(this, "_signclick")),
                on(this.switchButtonNode,"click", lang.hitch(this, "_switchclick"))
            );
        }
    });
});