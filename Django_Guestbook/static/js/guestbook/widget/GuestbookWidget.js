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
    "dijit/_WidgetsInTemplateMixin",
    "dijit/form/Button",
    "dijit/form/ValidationTextBox",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare, baseFx, lang, mouse, on, _WidgetBase, arrayUtil, GreetingWidget, _TemplatedMixin,
            dom, request, notify, parser, ready, cookie, domAtt, domConstruct, _WidgetsInTemplateMixin, button, validationtextbox, template){
    return declare("app.FirstWidget",[_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
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
                var arraywidget = [];
                arrayUtil.forEach(data.greetings, function(greeting){
                    greeting.is_admin = data.is_admin;
                    greeting.guestbook_name = data.guestbook_name
                    var widget = new GreetingWidget(greeting);
                    widget.placeAt(newDocFrag);
                    arraywidget.push(widget);
                });
                domConstruct.place(newDocFrag, greetingContainer);
                arrayUtil.forEach(arraywidget, function(widget){
                   widget.startup();
                });
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