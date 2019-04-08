from highcharts import Highchart
from data import class_percent

#creating an instance of Highchart class
chart = Highchart()

def draw_piechart():
	"""a function to create a line chart using chart object from Highchart class"""
	pos_sentiment, neg_sentiment = class_percent()
	options = {
		'chart': {
			'type': 'pie',
			'options3d': {
				'enabled': True,
				'alpha': 45,
				'beta': 0
				} 
			},
		'title': {
				'text': 'Sentiment Polarity Percentage'
			},
		'tooltip': {
				'valueSuffix': '%'
			},
		'plotOptions':{
			'pie': {
				'allowPointSelect': True,
				'cursor': 'pointer',
				'depth': 35,
				'dataLabels': {
					'enabled': True,
					'format': '{point.name}'
				}
			}	
		}
	}	
	data = [{
		'y': pos_sentiment
		},

		{
		'y': neg_sentiment,
		'sliced': True,
		'selected': True
	}]
	categories = ['Positive Polarity', 'Negative Polarity']
	sent_data = []
	for a in range(len(data)):
		sent_data.append({
			'name': categories[a],
			'y': data[a]['y']
			
		})	
	chart.set_dict_options(options)
	chart.add_data_set(sent_data, 'pie', 'Percentage')
	chart.save_file('templates/pie_highchart')

if __name__ == '__main__':
	draw_piechart()

