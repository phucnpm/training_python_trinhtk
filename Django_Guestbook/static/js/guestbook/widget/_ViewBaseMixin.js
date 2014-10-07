define([
	'dojo/_base/declare',
	'dojo/dom-class',
	'dojo/_base/lang',
	'dijit/_TemplatedMixin',
	'dijit/_WidgetsInTemplateMixin',
    'dijit/_WidgetBase'
], function(declare, domClass, lang, _TemplatedMixin, _WidgetsInTemplateMixin, _WidgetBase) {

	return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
		_watches: null,

		constructor: function() {
			this._watches = [];
		},

		uninitialize: function() {
			var w = this._watches.pop();
			while (w) {
				w.unwatch();
				w = this._watches.pop();
			}
			return false;
		},

		_watch: function(stateful, name, callback) {
			var handle = stateful.watch(name, lang.hitch(this, callback));
			this._watches.push(handle);
			return handle;
		},
		buildRendering: function() {
			this.inherited(arguments);
			this._appendClass();
		},

		_appendClass: function() {
			var parts = this.declaredClass.split('.'),
				baseClass = parts[parts.length - 1];
			baseClass = baseClass.substring(0, 1).toLowerCase() + baseClass.substring(1);
            domClass.add(this.domNode, baseClass);
		}
	});
});

