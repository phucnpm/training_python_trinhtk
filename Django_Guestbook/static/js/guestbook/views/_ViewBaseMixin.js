define([
	'dojo/_base/declare',
	'dojo/dom-class',
	'dijit/_TemplatedMixin',
	'dijit/_WidgetsInTemplateMixin'
], function(declare, domClass, _TemplatedMixin, _WidgetsInTemplateMixin) {

	return declare([_TemplatedMixin, _WidgetsInTemplateMixin], {
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

