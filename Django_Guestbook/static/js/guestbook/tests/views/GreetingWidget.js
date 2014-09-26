define([
    'doh',
    'dojo/json',
    'dojo/dom',
    '../sinon',
    'dojo/dom-attr',
    '../../widget/GreetingWidget'
], function(doh, json, dom, sinon, domAttr, GreetingWidget){
    doh.register('guestbook.widget.GreetingWidget', {
            name : "Show_button_delete_when_admin_logged_in",
            setUp: function(){

            },
            tearDown: function () {
                this.GreetingWidget.destroy();
            },
            runTest: function(){
                var greeting = {'is_admin': 'true'};
                var deferred = new doh.Deferred();
                this.GreetingWidget = new GreetingWidget(greeting);
                obj = this;
                var deleteButtonNode_style_visibility = obj.GreetingWidget.deleteButtonNode.domNode.style.visibility;
                doh.is(deleteButtonNode_style_visibility, "visible");
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
                var greeting = {'is_admin': 'true'};
                this.GreetingWidget = new GreetingWidget(greeting);
                var contentNode_disabled= domAttr.get(this.GreetingWidget.contentNode, "disabled");
                doh.is(contentNode_disabled,  false);
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
                var greeting = {'is_author': 'true'};
                var deferred = new doh.Deferred();
                this.GreetingWidget = new GreetingWidget(greeting);
                obj = this;
                var contentNode_disabled= domAttr.get(this.GreetingWidget.contentNode, "disabled");
                doh.is(contentNode_disabled,  false);
            },
            timeout: 5000
        }
    );


});