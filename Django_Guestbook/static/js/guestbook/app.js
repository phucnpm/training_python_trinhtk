define([
	'dojo/_base/lang',
	'dojo/_base/config',
	'dojo/parser',
	'dojo/ready',
	'dojo/hash',
	'dojo/io-query',
	'dojo/router',
	"dojo/dom",
	"dojo/dom-attr",
	"dojo/on",
	'./models/app'
], function(lang, config, parser, ready, hash, ioQuery, router, dom, domAttr, on, app) {

	router.register('posts', function(evt) {
		app.router = 'posts';
	});

	router.register('new', function(evt) {
		app.router = 'new';
	});

	router.register('post/:id', function(evt) {
		app.router = 'postsDetail';
		app.idGreeting = evt.params.id;
	});

	return function() {
		var prefix = '!',
			default_page = "posts";
		ready(function() {
			if (!config.parseOnLoad) {
				parser.parse();
			}
			router.startup();
			on(dom.byId("menu"), "a:click", function(event){
				event.preventDefault();
				var page = domAttr.get(this, "href").replace(".php", "");
				router.go(page);
			});
			hash((location.hash || default_page), true);
		});
	};
});
