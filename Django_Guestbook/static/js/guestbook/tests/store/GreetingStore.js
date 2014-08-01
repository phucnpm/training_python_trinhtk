define([
    'doh',
    'dojo/json',
    '../sinon',
    '../../models/GreetingStore'
], function(doh, json, sinon, GreetingStore){
    doh.register('guestbook.models.GreetingStore', {
            name : "Test_Get_Greeting",
            setUp: function(){
                this.server = sinon.fakeServer.create();
                this.server.respondWith("GET", "",
                [204, {"Content-Type": "application/json"},
                '[{ "id": 12, "comment" : "Hey there" }]']);

            },
            tearDown: function () {
                this.server.restore();
            },
            runTest: function(){
                var mydata;
                var deferred = new doh.Deferred();
                var myStore = new GreetingStore();
                myStore.getGreetings("default_guestbook", "None").
                    then(deferred.getTestCallback(
                            function(data){
                                mydata = data;
                                 doh.is(mydata, [{ id: 12, comment: "Hey there" }]);
                            })
                    );
                this.server.respond();
                return deferred;
            }
        }
    );
    doh.register('guestbook.models.GreetingStore', {
            name : "Test_reponse_server_failed",
            setUp: function(){
                this.server = sinon.fakeServer.create();
                this.server.respondWith('POST', '/api/guestbook/default_guestbook/greeting/', [
                    400,
                    {"Content-Type": "application/json"},
                    ''
                ]);
            },
            tearDown: function () {
                this.server.restore();
            },
            runTest: function(){
                var deferred = new doh.Deferred();
                var myStore = new GreetingStore();
                var status;
                myStore.addGreeting("my Content","default_guestbook").
                    then(
                        deferred.getTestCallback(function(content){
                            console.log(content);
                        }),
                        deferred.getTestCallback(function(error){
                            status = error.status;
                            doh.is(status, 400);
                        })
                );
                thisObject = this;
                setTimeout(function(){
                    thisObject.server.respond();
                }, 1000);
                return deferred;
            }
        }
    );
});