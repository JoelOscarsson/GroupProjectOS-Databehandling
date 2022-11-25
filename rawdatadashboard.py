import plotly_express as px
import pandas as pd
import numpy as np
import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/larkie11/pen/NJmbLx.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#MAIN DATA SET
aathlete_events =  pd.read_csv("Data/athlete_events.csv")
regions_athlete_events = pd.read_csv("Data/noc_regions.csv")
athlete_events = aathlete_events.merge(regions_athlete_events, on='NOC', how='left')
athlete_events.drop_duplicates(inplace=True)

#NAN SETS ARE NOT FILTERED OUT AS WE WANT ALL PARTICIPANTS EVEN IF THEY HAVE CERTAIN NAN COLUMNS
#WILL BE CHECKED IN THEIR OWN FIGURES/PLOTS/STATS

#DATASET FOR MEDALISTS

athlete_events = athlete_events.dropna(subset=['Medal'])
athlete_events= athlete_events.drop_duplicates(subset=['ID'])
malemedalists = athlete_events.loc[athlete_events['Sex']=='M']
femalemedalists = athlete_events.loc[athlete_events['Sex']=='F']

# FOR DROP DOWN IN STATS AREA, Getting all unique sports and medals into its own nparray
available_indicators = athlete_events['Sport'].unique()
available_indicators.sort()
available_indicators = np.append('All sports', available_indicators)
available_indicators2 = athlete_events['Medal'].unique()
available_indicators2 = np.append('All', available_indicators2)
available_indicators2 = np.append('None', available_indicators2)

# PARTICIPANTS OVER THE YEARS BY GENDER
genders = athlete_events.groupby(['Sex', 'Year'], as_index=False).size().reset_index()
# add count of females and males and their total each year
men = athlete_events[athlete_events['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()

women = athlete_events[athlete_events['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

total_athlete_events = men.merge(women, on='Year', how='left')
total_athlete_events.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
total_athlete_events.fillna(0, inplace=True)
total_athlete_events["Total"] = total_athlete_events["Male"] + total_athlete_events["Female"]


#MAIN LAYOUT
app.layout = html.Div([
	html.H1("Raw Data Statistics about the history of Olympics"),
    dcc.Dropdown(
        id="my-input",
        options = [
			{'label':'Statistics of participants in Olympics', 'value':'1'},
        ],
		#default value
        value = '1'
    ),
	html.Div(
        id="statistic_sports", 

		style={'textAlign':'center'},
        children = [
		html.H2("Statistics of unique participants in Olympics"),
		html.H3('All sports, unique participants from {} to {}'.format(genders.Year.min(),genders.Year.max())),
        html.P('Height Median: {0:.2f}'.format(athlete_events['Height'].median())),
        html.P('Height Mean: {0:.2f}'.format(athlete_events['Height'].mean())),
		html.P('Age Median: {0:.2f}'.format(athlete_events['Age'].median())),
        html.P('Age Mean: {0:.2f}'.format(athlete_events['Age'].mean())),
		html.P('Weight Median: {0:.2f}'.format(athlete_events['Weight'].median())),
        html.P('Weight Mean: {0:.2f}'.format(athlete_events['Weight'].mean())),
		html.P('Total Participants: {0:.0f}'.format(total_athlete_events['Total'].sum())),

		html.H4('Filter statistics'),
        dcc.Dropdown(
                id='dd_sports',
                options=[{'label': i, 'value': i} for i in available_indicators],
				value='',
                placeholder="Select a sport"
         ),
		dcc.Dropdown(
                id='dd_medal',
				options = [
            {'label':'No medals', 'value':'non-medalist'},
            {'label':'All participants', 'value':'participants'},
			{'label':'Gold', 'value':'Gold medalist'},
			{'label':'Silver', 'value':'Silver medalist'},
			{'label':'Bronze', 'value':'Bronze medalist'},],
				value='participant(s)',
                placeholder="Select the medal",
         ),
		dcc.Dropdown(
                id='dd_attributes',
                options = [
            {'label':'Age', 'value':'Age'},
            {'label':'Height/cm', 'value':'Height'},
			{'label':'Weight/KG', 'value':'Weight'},
        ],
		value='1',
        placeholder="Select an attribute",
		),
		dcc.Dropdown(
                id='dd_genders',
                options = [
            {'label':'All genders', 'value':''},
            {'label':'Female/F', 'value':'F'},
			{'label':'Male/M', 'value':'M'},
        ],
		value='',
        placeholder="Select a gender",
         ),
	]),
	html.Div(id='my-div'),
])

#MAIN UPDATE CALLBACKS
#Statistic page
@app.callback(Output(component_id='my-div', component_property='children'), [Input('my-input', 'value'),Input('dd_sports', 'value'),Input('dd_medal','value'),Input('dd_attributes','value'),Input('dd_genders','value')])
def update_plot(my_input,sports_input,medal_input,attributes_input,genders_input):
	text = ''
	filtered_athlete_events=athlete_events.copy()
	filtered_athlete_events['Medal'] = filtered_athlete_events['Medal'].fillna('None')	
	filtered_athlete_events['Height'] = filtered_athlete_events['Height'].fillna('None')	
	filtered_athlete_events['Weight'] = filtered_athlete_events['Weight'].fillna('None')	

	if my_input=='1':
		median = mean = -1
		print(sports_input)
		if (sports_input != 'All sports') and (sports_input != '1') :
			filtered_athlete_events = filtered_athlete_events[filtered_athlete_events.Sport == sports_input]
		if (medal_input!='participant(s)') and (medal_input!='non-medalist') and (medal_input!='all participants'):
			if (medal_input == 'Gold medalist'):
				filtered_athlete_events = filtered_athlete_events[filtered_athlete_events.Medal == 'Gold']
			if (medal_input == 'Silver medalist'):
				filtered_athlete_events = filtered_athlete_events[filtered_athlete_events.Medal == 'Silver']
			if (medal_input == 'Bronze medalist'):
				filtered_athlete_events = filtered_athlete_events[filtered_athlete_events.Medal == 'Bronze']
		if (medal_input=='non-medalist')and (medal_input!='all participants'):
			filtered_athlete_events = filtered_athlete_events[filtered_athlete_events.Medal == 'None']

		if (genders_input == 'F') or (genders_input =='M') :
			filtered_athlete_events = filtered_athlete_events[filtered_athlete_events.Sex == genders_input]

		#ATTRIBUTES ARE NEEDED FOR SHOWING STATS
		#NULL VALUES NOT DROPPED AS WE WANT THE NUMBER OF ALL PARTICIPANTS TO STAY CONSISTENT IN EACH ATTRIBUTE
		#EG. SOME PARTICIPANTS MAY HAVE ONLY AGE AND NOT THE REST AND THEY WILL BE DROPPED IN THE OTHER ATTRIBUTES
		if attributes_input =='Age':
			#filtered_athlete_events = filtered_athlete_events.dropna(subset=['Age'])
			filtered_athlete_events['Age'].replace('None', np.nan, inplace=True)			
			median = filtered_athlete_events['Age'].median()
			mean = filtered_athlete_events['Age'].mean()
		if attributes_input =='Height':
			filtered_athlete_events['Height'].replace('None', np.nan, inplace=True)	
			median = filtered_athlete_events['Height'].median()
			mean = filtered_athlete_events['Height'].mean()
		if attributes_input =='Weight':
			filtered_athlete_events['Weight'].replace('None', np.nan, inplace=True)	
			median = filtered_athlete_events['Weight'].median()
			mean = filtered_athlete_events['Weight'].mean()
		
		if (sports_input == 'All sports') or (sports_input == '1'):
			if (median >= 0) and (mean >= 0):
					return [
						html.P('{} statistics for all sports, {} {} {}'.format(attributes_input,filtered_athlete_events['ID'].count(),medal_input,genders_input)),
						html.P('Median: {0:.2f}'.format(median)),
						html.P('Mean: {0:.2f}'.format(mean)),
						dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_athlete_events.columns],
								data=filtered_athlete_events.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
						]
		elif (sports_input != 'All sports') and (sports_input != '1'):
			if (median >= 0) and (mean >= 0):
				
				return [
							html.P('{} statistics for {}, {} {} {}'.format(attributes_input,sports_input, filtered_athlete_events['ID'].count(),medal_input, genders_input )),
							html.P('Median: {0:.2f}'.format(median)),
							html.P('Mean: {0:.2f}'.format(mean)),
							dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_athlete_events.columns],
								data=filtered_athlete_events.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
							]
			else:
				if (attributes_input!='1'):
					if (filtered_athlete_events['ID'].count() >= 1):
						return [
			html.P('{} statistics for {}, {} {} {}'.format(attributes_input,sports_input, filtered_athlete_events['ID'].count(),medal_input, genders_input )),
			html.P('Not enough data to calculate median and mean'),
			dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_athlete_events.columns],
								data=filtered_athlete_events.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
			]
		#SHOWS TABLE EVERYTIME DROP DOWN CHANGES
		if (filtered_athlete_events['ID'].count() >= 1):
			return [
					dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_athlete_events.columns],
								data=filtered_athlete_events.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
			]
		else:
			return [
			html.P('No results found'),
			html.P('Not enough data to calculate median and mean')]




if __name__ == '__main__':
	app.run_server()