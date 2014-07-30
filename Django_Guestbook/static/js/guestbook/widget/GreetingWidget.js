define([
    "dojo/cookie",
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dojo/dom-style",
    "dojo/mouse",
    "dojo/on",
    "./GuestbookWidget",
    "../models/GreetingStore",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/form/Button",
    "dijit/form/ValidationTextBox",
    "dijit/InlineEditBox",
    "dojo/text!./templates/GreetingWidget.html"
], function(cookie, declare, lang, domStyle, mouse, on,
            GreetingStore, GuestbookWidget, _WidgetBase, _TemplatedMixin,_WidgetsInTemplateMixin,
            Button, ValidationTextBox, InlineEditBox, template){
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        author: "An anonymous",
        content: "",
        pub_date: "",
        updated_by: "<Not updated>",
        date_modified: "<Not updated>",
        templateString: template,
        baseClass: "GreetingWidget",
        mouseAnim: null,
        baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",
        is_admin : false,
        guestbook_name : "",
        is_author : false,
        id_greeting : "",
        disabled: "",
        hidden : "none",
        avatar: require.toUrl("guestbook/widget/images/defaultAvatar.jpg"),

        postCreate: function(){
            var domNode = this.domNode;
            this.inherited(arguments);
            domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
            this.own(
                on(this.contentNode, "change", lang.hitch(this, "_put", this.guestbook_name, this.id_greeting)),
                on(this.deleteButtonNode,"click", lang.hitch(this, "_delete", this.guestbook_name, this.id_greeting)),
                on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
                on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor))
            );
        },

        buildRendering: function(){
            if(this.is_admin){
                this.hidden = "display: true";
            }
            else
                this.hidden = "display: none";
            if(this.is_admin || this.is_author){
                this.disabled = "disabled: false,"
            }
            else
                this.disabled = "disabled: true,";
            this.inherited(arguments);
        },

        _guestbook: function(){
            return dijit.byId("guestbook");
        },

        startup: function(){
            this.inherited(arguments);
        },
        _changeBackground: function(newColor) {
            if (this.mouseAnim) {
                this.mouseAnim.stop();
            }
            this.mouseAnim = baseFx.animateProperty({
                node: this.domNode,
                properties: {
                    backgroundColor: newColor
                },
                onEnd: lang.hitch(this, function() {
                    this.mouseAnim = null;
                })
            }).play();
        },

        _delete: function(guestbook, id){
            if(!this.is_admin){
                alert("You are not administrator!!!");
            }
            else{
                this._guestbook()._deletegreeting(id);
                this._guestbook()._loadgreeting(guestbook, 500);
            }


        },

        _put: function(guestbook, id){
            //this.contentNode.value
            if(this.is_admin || this.is_author){
                this._guestbook()._updategreeting(id, this.contentNode.value);
                this._guestbook()._loadgreeting(guestbook, 500);

            }
            else{
                alert("You don't have permisson to update this greeting!!")
            }

        },

        _setAvatarAttr: function(imagePath) {
            if (imagePath != "") {
                this._set("avatar", imagePath);
                this.avatarNode.src = imagePath;
            }
        }

    });
});