require([
        "dojo/dom-attr",
        "dojo/_base/declare",
        "dojo/_base/lang",
        "dojo/dom-construct",
        "dojo/dom",
        "dojo/cookie",
        "dojo/request",
        "dojo/parser",
        "dojo/ready",
        "dijit/form/Button",
        "dijit/layout/ContentPane",
        "dijit/form/SimpleTextarea",
        "dijit/_TemplatedMixin",
        "dojo/on",
        "dojo/_base/array",
        "guestbook/widget/GreetingWidget",
        "dojo/text!guestbook/widget/templates/GuestbookWidget.html",
        "dijit/_WidgetBase"],
    function (domAtt,declare,lang,domConstruct,dom,cookie,request,parser,ready,myButton,
              myContentPane,mySimpleText,_TemplatedMixin,on,arrayUtil,GreetingWidget,template, _WidgetBase){
        declare ("app.FirstWidget",[_WidgetBase],{
            guestbook : "No name",
            baseClass : "GuestbookWidget",
            templateString : template,
            constructor : function(){
                this.guestbook = "default_guestbook";
            },
            _click: function(guestbook){
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
            _setGuestbookAttr : function(guestbook){
                this.guestbook = guestbook;
            },
            postCreate : function(){
                alert("Hello");
                //Load 10 greetings of default_guestbook
                request("/api/guestbook/"+this.guestbook+"/greeting/", {
                    handleAs: "json"
                }).then(function(data){
                    var greetingContainer = dom.byId("greetingContainer");
                    arrayUtil.forEach(data.greetings, function(greeting){
                        var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
                    });
                });
            }

//            buildRendering : function(){
//                var guestbookContainer = new myContentPane({
//                    title: "Greetings",
//                    content: "Content:",
//                    id: "guestbook"
//                },"guestbook");
//                var signButton = new myButton({
//                    value: "Sign Guestbook",
//                    id: "signButton"
//                });
//                var content = new mySimpleText({
//                    name: "content",
//                    rows: "4",
//                    cols: "50",
//                    style: "width:auto;",
//                    id: "content"
//                });
//                guestbookContainer.addChild(content);
//                guestbookContainer.addChild(signButton);
//                guestbookContainer.startup();
//                on(signButton,"click", lang.hitch(this, "_click", this.guestbook))
//            },
        });

    });
