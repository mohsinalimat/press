<template>
	<div class="space-y-4">
		<div
			v-for="field in fields"
			:key="field.fieldname"
			v-show="field.condition ? field.condition() : true"
		>
			<div class="flex space-x-4" v-if="Array.isArray(field)">
				<FormControl
					v-bind="getBindProps(subfield)"
					:key="subfield.fieldname"
					class="w-full"
					v-for="subfield in field"
				/>
			</div>
			<FormControl v-else v-bind="getBindProps(field)" />
			<ErrorMessage
				class="mt-1"
				v-if="requiredFieldNotSet.includes(field)"
				error="This field is required"
			/>
		</div>
	</div>
</template>

<script>
// https://github.com/eggert/tz/blob/main/backward add more if required.
const TZ_BACKWARD_COMPATBILITY_MAP = {
	'Asia/Calcutta': 'Asia/Kolkata'
};

export default {
	name: 'Form',
	props: ['fields', 'modelValue'],
	emits: ['update:modelValue'],
	data() {
		return {
			requiredFieldNotSet: [],
			guessedTimezone: ''
		};
	},
	mounted() {
		this.guessedTimezone = this.guessTimezone();
	},
	watch: {
		fields: {
			handler(new_fields) {
				let timezoneFields = new_fields.filter(
					f => f.fieldtype === 'Select' && f.fieldname.endsWith('_tz')
				);
				for (let field of timezoneFields) {
					if (!field.options) {
						field.options = [];
					}
					if (
						this.guessedTimezone &&
						field.options.includes(this.guessedTimezone)
					) {
						this.onChange(this.guessedTimezone, field);
					}
				}
			},
			deep: true
		}
	},
	methods: {
		onChange(value, field) {
			this.checkRequired(field, value);
			this.updateValue(field.fieldname, value);
		},
		updateValue(fieldname, value) {
			let values = Object.assign({}, this.modelValue, {
				[fieldname]: value
			});
			this.$emit('update:modelValue', values);
		},
		checkRequired(field, value) {
			if (field.required) {
				if (!value) {
					this.requiredFieldNotSet.push(field);
					return false;
				} else {
					this.requiredFieldNotSet = this.requiredFieldNotSet.filter(
						f => f !== field
					);
				}
			}
			return true;
		},
		getBindProps(field) {
			return {
				label: field.label || field.fieldname,
				type: this.getInputType(field),
				options: field.options,
				name: field.fieldname,
				modelValue: this.modelValue[field.fieldname],
				disabled: field.disabled,
				required: field.required || false,
				rows: field.rows,
				placeholder: field.placeholder,
				'onUpdate:modelValue': value => this.onChange(value, field),
				onBlur: e => this.checkRequired(field, e)
			};
		},
		getInputType(field) {
			return {
				Data: 'text',
				Int: 'number',
				Select: 'select',
				Check: 'checkbox',
				Password: 'password',
				Text: 'textarea',
				Date: 'date'
			}[field.fieldtype || 'Data'];
		},
		guessTimezone() {
			try {
				let tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
				if (TZ_BACKWARD_COMPATBILITY_MAP[tz]) {
					return TZ_BACKWARD_COMPATBILITY_MAP[tz];
				}
				return tz;
			} catch (e) {
				console.error("Couldn't guess timezone", e);
				return null;
			}
		}
	}
};
</script>
