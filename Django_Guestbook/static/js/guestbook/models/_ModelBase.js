define([
	'dojo/_base/kernel',
	'dojo/_base/declare',
	'dojo/_base/lang',
	'dojo/date/stamp',
	'dojo/date/locale',
	'../support/dojo/Stateful',
	'../support/dojox/mvc/getStateful',
	'../support/dojox/mvc/getPlainValue'
], function(kernel, declare, lang, stamp, locale, Stateful, getStateful, getPlainValue) {
	// module:
	//		fasti/common/models/_ModelBase

	var _ModelBase = declare(Stateful, {

		set: function(name, value) {
			if (typeof name !== 'object') {
				value = getStateful(value, _ModelBase.getStatefulOptions);
			}
			return this.inherited(arguments, [name, value]);
		},

		toPlainObject: function() {
			return getPlainValue(this, _ModelBase.getPlainValueOptions);
		},

		getFormattedDate: function(name, /*dojo.date.locale.__FormatOptions?*/options) {
			// summary:
			//		get a formatted date string.
			//
			// TODO: Move to _TemplatedMixin
			var date = this.get(name);
			if (!date) return null;

			return locale.format(date, options);
		},

		deserializeToString: function(value) {
			if (value && typeof value !== 'string') {
				value = '' + value;
			}
			return value;
		},

		deserializeToDate: function(value) {
			if (value && !(value instanceof Date)) {
				value = stamp.fromISOString(value.replace(' ', 'T'));
			}
			return value;
		},

		serializeToISO: function(value, options) {
			return value instanceof Date ? stamp.toISOString(value, options) : value;
		},

		deserializeToModel: function(value, modelClass) {
			if (value && typeof value == 'object' && !(value instanceof modelClass)) {
				value = new modelClass(value);
			}
			return value;
		}
	});

	var Model = declare(_ModelBase, {
		// summary:
		//		Generic model class (for internal use).
	});

	lang.mixin(_ModelBase, {
		// getStatefulOptions: dojox.mvc.getStatefulOptions
		//		The options to get stateful object from plain value.
		getStatefulOptions: {
			getType: getStateful.getType,
			getStatefulArray: getStateful.getStatefulArray,
			getStatefulValue: getStateful.getStatefulValue,

			getStatefulObject: function(/*Object*/o) {
				// Return non plain objects as-is (Currently not strict)
				if (o.isInstanceOf) {
					return o;
				}

				var model = new Model();
				for (var s in o) {
					model[s] = getStateful(o[s], this);
				}
				return model;
			}
		},

		// getPlainValueOptions: dojox.mvc.getPlainValueOptions
		//		The options to get plain value from stateful object.
		getPlainValueOptions: {
			getType: getPlainValue.getType,
			getPlainArray: getPlainValue.getPlainArray,
			getPlainValue: getPlainValue.getPlainValue,

			getPlainObject: function(/*Object*/o) {
				// summary:
				//		Return a plain object; Only return non-private properties.
				//
				var plain = {},
					object = 'object',
					s, v;
				for (s in o) {
					if (s[0] === '_' || s in _ModelBase.prototype || s.toUpperCase() == s) {
						continue;
					}

					v = o[s];

					if (lang.isFunction(v)) {
						continue;
					}

					if (v && this.getType(v) === object) {
						if (!v.isInstanceOf || !v.isInstanceOf(_ModelBase)) {
							// Skip non Model instances
							//  (e.g. stores which is typically set by ModelBind)
							continue;
						}
					}
					plain[s] = getPlainValue(o[s], this);
				}
				return plain;
			}
		}
	});

	return _ModelBase;
});
