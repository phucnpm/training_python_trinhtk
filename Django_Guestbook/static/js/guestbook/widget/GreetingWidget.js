define([
    "dojo/request",
    "dojo/parser",
    "dojo/ready",
    "dojo/cookie",
    "dojo/_base/declare",
    "dojo/_base/fx",
    "dojo/_base/lang",
    "dojo/dom-style",
    "dojo/mouse",
    "dojo/on",
    "guestbook/widget/GuestbookWidget",
    "dijit/_WidgetBase",
    "dijit/_OnDijitClickMixin",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/form/Button",
    "dijit/form/ValidationTextBox",
    "dijit/InlineEditBox",
    "dijit/form/Textarea",
    "dojo/fx/Toggler",
    "dojo/text!./templates/GreetingWidget.html"
], function(request, parser, ready, cookie, declare, baseFx, lang, domStyle, mouse, on,
            GuestbookWidget, _WidgetBase, _OnDijitClickMixin, _TemplatedMixin,_WidgetsInTemplateMixin,
            Button, ValidationTextBox, InlineEditBox, Textarea, Toggler, template){
    return declare([_WidgetBase,_OnDijitClickMixin, _TemplatedMixin, _WidgetsInTemplateMixin], {
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
                request.del("/api/guestbook/"+guestbook+"/greeting/"+id+"/", {
                    headers:{
                        "X-CSRFToken": cookie('csrftoken')
                    },
                    timeout : 1000
                });
                dijit.byId("guestbook")._loadgreeting(guestbook, 500);
            }


        },

        _put: function(guestbook, id){
            //this.contentNode.value
            if(this.is_admin || this.is_author){
                request.put("/api/guestbook/"+guestbook+"/greeting/"+id+"/", {
                    data:{
                        content: this.contentNode.value
                    },
                    headers:{
                        "X-CSRFToken": cookie('csrftoken')
                    },
                    timeout : 1000
                });
                dijit.byId("guestbook")._loadgreeting(guestbook, 500);

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