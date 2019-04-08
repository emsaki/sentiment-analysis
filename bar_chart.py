from highcharts import Highchart
from data_charts import get_data


chart = Highchart()


def draw_barchart():	
	c1, c2, c3, cat = get_data()
	
	options = {
		'chart':{'type':'bar'},
		'title':{'text':'Bar Chart Exploratory Visualization'},
		'legend':{'enabled':True},
		'xAxis':{'categories':cat},
		'yAxis':{'title':{'Record Counts'}},
		}

	chart.set_dict_options(options)

	chart.add_data_set(c1, 'bar', 'Followers Count')
	chart.add_data_set(c2, 'bar', 'Friends Count')
	chart.add_data_set(c3, 'bar', 'Statuses Count')
	chart.save_file('templates/bar_highchart')
	

if __name__ == '__main__':
	draw_barchart()