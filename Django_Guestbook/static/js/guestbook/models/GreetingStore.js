define([
    'dojo/request',
    'dojo/cookie',
    'dojo/dom',
    'dojo/_base/array',
    'dojo/_base/declare',
    'dojo/store/JsonRest',
    'dojo/Stateful'
], function(request, cookie, dom, array, declare, JsonRest, Stateful) {
    return declare([Stateful], {
        guestBookName: '',
        store: null,

        _guestBookNameGetter: function(){
            return this.guestBookName;
        },

        _guestBookNameSetter: function(value){
            this.guestBookName = value;
        },

        constructor: function(){
            this.inherited(arguments);

            // update target when guestBookName change
            this.watch('guestBookName', function(name, oldValue, value){
                if(oldValue != value)
                {
                    console.log('guestBookName changed');
                    var url = "/api/guestbook/"+value+"/greeting/";
                    this.store = new JsonRest({
                        target: url,
                        headers: {
                            "X-CSRFToken": cookie("csrftoken")
                        }
                    });
                }
            });
        },

        getGreetings: function(guestBookName, cursor){
            this.set('guestBookName', guestBookName);
            return this.store.query({
                cursor: cursor
            })
        },

        deleteGreeting: function(greetingId, guestBookName){
            this.set('guestBookName', guestBookName);
            return this.store.remove(greetingId);
        },

        addGreeting: function(greetingContent, guestBookName){
            this.set('guestBookName', guestBookName);
            greeting = {
                content: greetingContent
            };
            return this.store.add(greeting);
        },

        updateGreeting: function(greetingId, greetingContent, guestBookName){
            this.set('guestBookName', guestBookName);
            greeting = {
                id: greetingId,
                content: greetingContent,
                guestbook_name: guestBookName
            };
            return this.store.put(greeting);
        }
    });
});
