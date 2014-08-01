define([
    'doh',
    'dojo/json',
    'dojo/dom',
    '../sinon',
    '../../widget/GreetingWidget'
], function(doh, json, dom, sinon, GreetingWidget){
    doh.register('guestbook.widget.GreetingWidget', {
            name : "Show_button_delete_when_admin_logged_in",
            setUp: function(){

            },
            tearDown: function () {
                this.GreetingWidget.destroy();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                this.GreetingWidget = new GreetingWidget(true, false);//Fake is admin
                obj = this;
                setTimeout(deferred.getTestCallback(function(){
                    var deleteButtonNode_style_visibility = obj.GreetingWidget.deleteButtonNode.domNode.style.visibility;
                    console.log(deleteButtonNode_style_visibility);
                    doh.is(deleteButtonNode_style_visibility, "visible");
                }), 100 );
                return deferred;
            },
            timeout: 5000
        }
    );
    doh.register('guestbook.widget.GreetingWidget', {
            name : "Active_edit_inline_when_admin_logged_in",
            setUp: function(){

            },
            tearDown: function () {
                this.GreetingWidget.destroy();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                this.GreetingWidget = new GreetingWidget(true, false);//Fake is admin
                obj = this;
                setTimeout(deferred.getTestCallback(function(){
                    var contentNode_disabled= obj.GreetingWidget.disabled;
                    console.log(contentNode_disabled);
                    doh.is(contentNode_disabled, "disabled: false,");
                }), 100 );
                return deferred;
            },
            timeout: 5000
        }
    );
    doh.register('guestbook.widget.GreetingWidget', {
            name : "Active_edit_inline_when_author_logged_in",
            setUp: function(){

            },
            tearDown: function () {
                this.GreetingWidget.destroy();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                this.GreetingWidget = new GreetingWidget(false, true);//Fake is author
                obj = this;
                setTimeout(deferred.getTestCallback(function(){
                    var contentNode_disabled= obj.GreetingWidget.disabled;
                    console.log(contentNode_disabled);
                    doh.is(contentNode_disabled, "disabled: false,");
                }), 100 );
                return deferred;
            },
            timeout: 5000
        }
    );


});