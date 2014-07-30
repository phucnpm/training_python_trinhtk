define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dojo/on",
    "dijit/_WidgetBase",
    "dojo/_base/array",
    "./GreetingWidget",
    "../models/GreetingStore",
    "dijit/_TemplatedMixin",
    "dojo/dom",
    "dojo/cookie",
    "dojo/dom-construct",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/form/Button",
    "dijit/form/ValidationTextBox",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare, lang, on, _WidgetBase, arrayUtil, GreetingWidget, GreetingStore, _TemplatedMixin,
            dom, cookie, domConstruct, _WidgetsInTemplateMixin, button, validationtextbox, template){
    return declare("app.FirstWidget",[_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        guestbook : "default_guestbook",
        templateString: template,
        baseClass: "GuestbookWidget",
        store : null,

        constructor : function(name){
            this.inherited(arguments);
            this.store = new GreetingStore();
        },

        _signclick: function(evt){
            text = this.contentNode.value;
            if (text.length > 10){
                alert("Max length = 10!!!");
            }
            else {
                if (text.length == 0){
                    alert("This field is required!");
                }
                else{
                    this._addgreeting();
                    this._loadgreeting(this.guestbook, 500);
                }
            }

        },

        _switchclick: function(){
            this.guestbook = this.guestbookNode.value;
            this._loadgreeting(this.guestbook, 0);
        },

        _loadgreeting: function(guestbook, time){
            var start = new Date().getTime();
            while (new Date().getTime() < start + time);
            this.greetingListNode.innerHTML = "";

            this.store.getGreetings(this.guestbook).then(
                function(data){
                    var greetingContainer = this.greetingListNode;
                    var newDocFrag = document.createDocumentFragment();
                    var arraywidget = [];
                    arrayUtil.forEach(data.greetings, function(greeting){
                        console.log(greeting);
                        greeting.is_admin = data.is_admin;
                        greeting.guestbook_name = data.guestbook_name;
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

        _addgreeting: function(){
            this.store.addGreeting(this.contentNode.value, this.guestbook);
        },

        _deletegreeting: function(greetingId){
            this.store.deleteGreeting(greetingId, this.guestbook)
        },

        _updategreeting: function(greetingId, greetingContent){
            this.store.updateGreeting(greetingId, greetingContent, this.guestbook)
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