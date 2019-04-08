from highcharts import Highchart
from data_charts import get_data

#creating an instance of Highchart class
chart = Highchart()

def draw_linechart():
	"""a function to create a line chart using chart object from Highchart class"""
	c1, c2, c3, cat = get_data()
	
	options = {
		'chart':{'type':'line'},
		'title':{'text':'Line Chart Exploratory Visualization'},
		'legend':{'enabled':True},
		'xAxis':{'categories':cat},
		'yAxis':{'title':{'Record Counts'}}
		}

	chart.set_dict_options(options)

	chart.add_data_set(c1, 'line', 'Followers Count')
	chart.add_data_set(c2, 'line', 'Friends Count')
	chart.add_data_set(c3, 'line', 'Statuses Count')
	chart.save_file('templates/line_highchart')

if __name__ == '__main__':
	draw_linechart()