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
	'dojo/router',
	'dojo/dom-style',
	"dojo/hash",
	"dojo/topic",
	"dojo/dom-attr",
	"dojo/text!./templates/GuestbookWidget.html"
], function(declare, lang, on, arrayUtil, GreetingWidget, GreetingStore,
			dom, cookie, domConstruct, button, validationtextbox,_ViewBaseMixin, router, domStyle, hash, topic, domAttr, template){
	//Show greetings

	return declare("app.FirstWidget",[_ViewBaseMixin], {
		guestbook : "default_guestbook",
		templateString: template,
		baseClass: "GuestbookWidget",
		store : null,
		autoload : true,

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
			this.guestbook = this.guestbookNode.value;
			this._loadgreeting(this.guestbook, 0);
		},

		_loadgreeting: function(guestbook, time){
			if (this.autoload){
				var start = new Date().getTime();
				while (new Date().getTime() < start + time);
				this.greetingListNode.innerHTML = "";
				console.log("INSIDE LOAD GREETING");
				var greetingContainer = this.greetingListNode;

				this.store.getGreetings(this.guestbook).then(
						function(data){
							var newDocFrag = document.createDocumentFragment();
							var arraywidget = [];
							arrayUtil.forEach(data.greetings, function(greeting){
								greeting.is_admin = data.is_admin;
								greeting.guestbook_name = data.guestbook_name;
								var widget = new GreetingWidget(greeting);
								widget.placeAt(newDocFrag);
								arraywidget.push(widget);
							});
							domConstruct.place(newDocFrag, greetingContainer);
							arrayUtil.forEach(arraywidget, function(widget){
								widget.startup();
							});
						},
						function(error){
							alert("ERROR!");
						}
				);

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

		route: function(){
			var prefix = '!',
				guestbook = this,
				lastPage = "posts";
			router.register("posts", function(evt){
				domStyle.set(dom.byId("idPost"), "display", "none");
				domStyle.set(dom.byId("idGreeting"), "display", "block");
				domStyle.set(dom.byId("idGreetingDetails"), "display", "none");

			});
			//Show post area
			router.register("new", function(evt){
				domStyle.set(dom.byId("idPost"), "display", "block");
				domStyle.set(dom.byId("idGreeting"), "display", "none");
				domStyle.set(dom.byId("idGreetingDetails"), "display", "none");
			});
			//Show post detail
			router.register("post/:id", function(evt){
				guestbook.loaddetailgreeting(evt.params.id, guestbook.guestbook, 0);
				domStyle.set(dom.byId("idPost"), "display", "none");
				domStyle.set(dom.byId("idGreeting"), "display", "none");
				domStyle.set(dom.byId("idGreetingDetails"), "display", "block");
			});
			router.startup();
			on(dom.byId("menu"), "a:click", function(event){
				event.preventDefault();
				var page = domAttr.get(this, "href").replace(".php", "");
				router.go(page);
			});
			hash((location.hash || lastPage), true);
		},

		postCreate: function(){
			this.inherited(arguments);
			domStyle.set(dom.byId("idGreeting"), "display", "none");
			domStyle.set(dom.byId("idGreetingDetails"), "display", "none");
			this.store = new GreetingStore();
			this.guestbookNode.value = this.guestbook;
			this._loadgreeting(this.guestbook, 0);
			this.route();
			this.own(
					on(this.signButtonNode,"click", lang.hitch(this, "_signclick")),
					on(this.switchButtonNode,"click", lang.hitch(this, "_switchclick"))
			);
		}
	});
});