define([
    'doh',
    'dojo/json',
    'dojo/dom',
    '../sinon',
    '../../widget/GuestbookWidget'
], function(doh, json, dom, sinon, GuestbookWidget){
//    Test load widget greeting in widget guestbook (if greetingListNode has 10 child -> loaded
    doh.register('guestbook.widget.GuestbookWidget', {
            name : "Test_load_greetingContainer",
            setUp: function(){

            },
            tearDown: function () {
                this.guestbookwidget.destroy();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                this.guestbookwidget = new GuestbookWidget("default_guestbook", true);
                obj = this;
                setTimeout(deferred.getTestCallback(function(){
                    var greetingContainer = obj.guestbookwidget.greetingListNode;
                    doh.is(greetingContainer.childElementCount, 10);
                }), 2000 );
                return deferred;
            },
            timeout: 5000
        }
    );
    doh.register('guestbook.widget.GuestbookWidget', {
            name : "Test_Sign_Button",
            setUp: function(){

            },
            tearDown: function () {
                this.guestbookwidget.destroy();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                this.guestbookwidget = new GuestbookWidget("default_guestbook", false);
                var spy = sinon.spy(this.guestbookwidget, "_signclick");
                obj = this;
                setTimeout(deferred.getTestCallback(function(){
                    obj.guestbookwidget.signButtonNode.onClick();
                    doh.is(spy.callCount, 1);
                }), 200);
                return deferred;
            },
            timeout: 5000
        }
    );
        doh.register('guestbook.widget.GuestbookWidget', {
            name : "Test_Switch_Button",
            setUp: function(){

            },
            tearDown: function () {
                this.guestbookwidget.destroy();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                this.guestbookwidget = new GuestbookWidget("default_guestbook", false);
                var spy = sinon.spy(this.guestbookwidget, "_switchclick");
                obj = this;
                setTimeout(deferred.getTestCallback(function(){
                    obj.guestbookwidget.switchButtonNode.onClick();
                    doh.is(spy.callCount, 1);
                }), 200);
                return deferred;
            },
            timeout: 5000
        }
    );

});