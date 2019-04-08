from wtforms import Form, StringField, validators

class TweetSearchForm(Form):
	search = StringField('', [validators.DataRequired()])