define([
    "dojo/cookie",
    "dojo/_base/fx",
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dojo/dom-style",
    "dojo/mouse",
    "dojo/on",
    "./GuestbookWidget",
    "../models/GreetingStore",
    "./_ViewBaseMixin",
    "dijit/form/Button",
    "dijit/form/ValidationTextBox",
    "dijit/InlineEditBox",
    "dojo/text!./templates/GreetingWidget.html"
], function(cookie, baseFx, declare, lang, domStyle, mouse, on,
            GreetingStore, GuestbookWidget, _ViewBaseMixin,
            Button, ValidationTextBox, InlineEditBox, template){
    return declare([_ViewBaseMixin], {
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
        avatar: require.toUrl("guestbook/widget/images/defaultAvatar.jpg"),

        constructor: function(admin, author){
            this.is_admin = admin;
            this.is_author = author;
        },

        postCreate: function(){
            if(this.is_admin){
                domStyle.set(this.deleteButtonNode.domNode, 'visibility', 'visible');
            }
            this.inherited(arguments);
            var domNode = this.domNode;
            domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
            this.own(
                on(this.contentNode, "change", lang.hitch(this, "_put", this.guestbook_name, this.id_greeting)),
                on(this.deleteButtonNode,"click", lang.hitch(this, "_delete", this.guestbook_name, this.id_greeting)),
                on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
                on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor))
            );
        },

        buildRendering: function(){
            console.log("BUILD RENDERING");
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