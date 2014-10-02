define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/on",
	"dojo/_base/array",
	"./GreetingWidget",
	"../models/GreetingStore",
	"dojo/dom",
	"dojo/cookie",
	"dojo/dom-construct",
	"dijit/form/Button",
	"dijit/form/ValidationTextBox",
	'./_ViewBaseMixin',
	'../common/views/_ListViewMixin',
	'dojo/router',
	'dojo/dom-style',
	"dojo/hash",
	"dojo/topic",
	"dojo/dom-attr",
	'dojo/_base/Deferred',
	'../models/app',
	"dojo/text!./templates/GuestbookWidget.html"
], function(declare, lang, on, arrayUtil, GreetingWidget, GreetingStore,
			dom, cookie, domConstruct, button, validationtextbox,_ViewBaseMixin,
			_ListViewMixin, router, domStyle, hash, topic, domAttr, Deferred, app, template){
	//Show greetings

	return declare("app.FirstWidget",[_ListViewMixin], {
		guestbook : "default_guestbook",
		templateString: template,
		baseClass: "GuestbookWidget",
		store : null,
		autoload : true,
		autoPaging: 10,
		cursor: null,
		model : app,

		_signclick: function(){
			text = this.contentNode.value;
			if (text.length > 10){
				alert("Max length = 10!!!");
				return -1;
			}
			else {
				if (text.length == 0){
					alert("This field is required!");
					return 0;
				}
				else{
					this._addgreeting();
					this._loadgreeting(this.guestbook, 500);
					return 1;
				}
			}

		},

		_switchclick: function(){
			this._loadgreeting(this.guestbook, 0);
		},

		_loadgreeting: function(guestbook, time){
			if (this.autoload){
				var start = new Date().getTime();
				while (new Date().getTime() < start + time);
				this.greetingListNode.innerHTML = "";
				this.cursor = null;
				this.guestbook = this.guestbookNode.value;
				this.loadItems({forceNew: true});
			}
		},

		loaddetailgreeting: function(id, guestbook, time){
			if (this.autoload){
				var start = new Date().getTime();
				while (new Date().getTime() < start + time);
				this.greetingDetailsNode.innerHTML = "";
				var greetingContainer = this.greetingDetailsNode;
				this.store.getGreeting(id, guestbook).then(
						function(data){
							var newDocFrag = document.createDocumentFragment();
							var greeting = data.greetings;
								greeting.is_admin = data.is_admin;
								greeting.guestbook_name = data.guestbook_name;
							var widget = new GreetingWidget(greeting);
								widget.placeAt(newDocFrag);
							domConstruct.place(newDocFrag, greetingContainer);
							widget.startup();
						},
						function(error){
							alert("ERROR!");
						}
				);

			}
		},

		_addgreeting: function(){
			var guestbook = this;
			this.store.addGreeting(this.contentNode.value, this.guestbook).then(
					function(result){
						var page = "post/" + result.id_greeting;
						router.go(page);
					}
			);
		},

		_deletegreeting: function(greetingId){
			this.store.deleteGreeting(greetingId, this.guestbook)
		},

		_updategreeting: function(greetingId, greetingContent){
			this.store.updateGreeting(greetingId, greetingContent, this.guestbook)
		},

		generate: function(value){
			var guestbook = this;
			switch (value) {
				case 'posts':
					domStyle.set(dom.byId("idPost"), "display", "none");
					domStyle.set(dom.byId("idGreeting"), "display", "block");
					domStyle.set(dom.byId("idGreetingDetails"), "display", "none");
					break;
				case 'new':
					domStyle.set(dom.byId("idPost"), "display", "block");
					domStyle.set(dom.byId("idGreeting"), "display", "none");
					domStyle.set(dom.byId("idGreetingDetails"), "display", "none");
					break;
				case 'postsDetail':
					guestbook._watch(this.model, 'idGreeting', function(name, oldValue, value) {
						guestbook.loaddetailgreeting(value, guestbook.guestbook, 0);
					});
					domStyle.set(dom.byId("idPost"), "display", "none");
					domStyle.set(dom.byId("idGreeting"), "display", "none");
					domStyle.set(dom.byId("idGreetingDetails"), "display", "block");
			}
		},

		fetchItems: function(options){
			var items = this.store.getGreetings(this.guestbook, options.cursor),
				greeting_list = items.greetings;
			arrayUtil.forEach(greeting_list, function(greeting){
								greeting.is_admin = items.is_admin;
								greeting.guestbook_name = items.guestbook_name;
							});
			return items;
		},

		getItemView: function(greeting) {
			return new GreetingWidget(greeting);
		},

		loadItems: function(options) {
			// Override
			var options = options || {},
				guestbookWidget = this,
				forceNew = options.forceNew || false;
			options.limit = options.limit || 10;
			options.cursor = guestbookWidget.cursor;

			return Deferred.when(this.fetchItems(options), lang.hitch(this, function(items) {
				if (items.greetings && items.greetings.length === options.limit) {
					arrayUtil.forEach(items.greetings, function(greeting){
						greeting.is_admin = items.is_admin;
						greeting.guestbook_name = items.guestbook_name;
					});
					this.set('pagingOption', {
						'limit': options.limit
					});
					guestbookWidget.cursor = items.cursor;
				}
				this.set('lastItems', items.greetings);
			}));
		},

		postCreate: function(){
			this.store = new GreetingStore();
			this.guestbookNode.value = this.guestbook;
			this.inherited(arguments);
			console.log("postCreate GuestbookWidget");
			console.log(this.model);
			domStyle.set(dom.byId("idGreeting"), "display", "none");
			domStyle.set(dom.byId("idGreetingDetails"), "display", "none");
			this.own(
					on(this.signButtonNode,"click", lang.hitch(this, "_signclick")),
					on(this.switchButtonNode,"click", lang.hitch(this, "_switchclick"))
			);
			this._watch(this.model, 'router', function(name, oldValue, value) {
					this.generate(value);
			});
		}
	});
});