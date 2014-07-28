define([
    "dojo/request",
    "dojo/cookie",
    "dojo/_base/declare",
    "dojo/_base/fx",
    "dojo/_base/lang",
    "dojo/dom-style",
    "dojo/mouse",
    "dojo/on",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/form/Button",
    "dojo/text!./templates/GreetingWidget.html"
], function(request, cookie, declare, baseFx, lang, domStyle, mouse, on, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,
            Button, template){
    return declare([_WidgetBase, _TemplatedMixin], {
        author: "No name",
        content: "",
        pub_date: "",
        last_udated: "",
        date_modified: "",
        templateString: template,
        baseClass: "GreetingWidget",
        mouseAnim: null,
        baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",
        is_admin : false,
        guestbook_name : "",
        id_greeting : "",

        postCreate: function(){
            this.deleteButtonNode.disabled = true;
            if (this.is_admin){
                this.deleteButtonNode.disabled = false;
            }
            var domNode = this.domNode;
            this.inherited(arguments);
            domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
            this.own(
                on(this.deleteButtonNode,"click", lang.hitch(this, "_delete", this.guestbook_name, this.id_greeting)),
                on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
                on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor))
            );
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
            alert(guestbook);
            alert(id);
            request.del("/api/guestbook/"+guestbook+"/greeting/"+id+"/", {
                headers:{
                    "X-CSRFToken": cookie('csrftoken')
                },
                timeout : 1000
            });
            alert("deleted");
        }

    });
});