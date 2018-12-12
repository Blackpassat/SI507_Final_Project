import sqlite3 as sqlite
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

current_season = '2015/2016'

class Player:
	def __init__(self, player_id):
		self.player_id = player_id

	def get_name(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT player_name FROM Player WHERE player_api_id=?
		'''
		result = cur.execute(statement, (self.player_id,)).fetchone()
		conn.close()
		return result[0]

	def get_age(self):
		global current_season
		season = current_season[5:]
		season += '-05-30'
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT strftime('%Y', ?) - strftime('%Y', birthday) FROM Player WHERE player_api_id=?
		'''
		result = cur.execute(statement, (season, self.player_id,)).fetchone()
		conn.close()
		return result[0]

	def get_general_info(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT height, weight FROM Player WHERE player_api_id=?
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		return result[0]

	def get_general_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT overall_rating, potential, preferred_foot
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		return result[0]

	def draw_attr(self, data, theta, title):
		data_list = []
		for d in data[0]:
			data_list.append(d)
		data_list.append(data_list[0])
		data = [go.Scatterpolar(
		  r = data_list,
		  theta = theta,
		  fill = 'toself'
		)]

		layout = go.Layout(
		  polar = dict(
		    radialaxis = dict(
		      visible = True,
		      range = [0, 100]
		    )
		  ),
		  showlegend = False,
		  paper_bgcolor='#D2FDFF',
	      plot_bgcolor='#D2FDFF',
	      title=title
		)

		fig = go.Figure(data=data, layout=layout)
		div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True, image_width=200, image_height=200)
		return div

	def get_attack_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT crossing, finishing, heading_accuracy, short_passing, volleys
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['Crossing', 'Finishing', 'Heading_Accuracy', 'Short Passing', 'Volleys']
		title = 'Attacking Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig

	def get_skill_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT dribbling, curve, free_kick_accuracy, long_passing, ball_control
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['Dribbling', 'Curve', 'Free Kick Accuracy', 'Long Passing', 'Ball Control']
		title = 'Skill Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig

	def get_move_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT acceleration, sprint_speed, agility, reactions, balance
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance']
		title = 'Movement Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig

	def get_power_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT shot_power, jumping, stamina, strength, long_shots
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots']
		title = 'Power Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig

	def get_ment_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT aggression, interceptions, positioning, vision, penalties
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties']
		title = 'Mentality Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig

	def get_def_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT marking, standing_tackle, sliding_tackle
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['Marking', 'Standing Tackle', 'Sliding Tackle']
		title = 'Defending Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig

	def get_gk_attr(self):
		conn = sqlite.connect('database.sqlite')
		cur = conn.cursor()
		statement = '''
			SELECT gk_diving, gk_handling, gk_kicking, gk_positioning, gk_reflexes
			FROM Player_Attributes
			WHERE player_api_id=?
			ORDER BY date desc
			LIMIT 1
		'''
		result = cur.execute(statement, (self.player_id,)).fetchall()
		conn.close()
		theta = ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']
		title = 'Goalkeeping Attributes'
		fig = self.draw_attr(result, theta, title)
		return fig



def get_seasons():
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT DISTINCT season FROM Match
	'''
	cur.execute(statement)
	result = []
	for row in cur:
		result.append(row[0])
	conn.close()
	return result

def get_leagues():
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT id, name FROM League
	'''
	cur.execute(statement)
	ids = []
	names = []
	for row in cur:
		ids.append(row[0])
		names.append(row[1])
	conn.close()
	# print(ids)
	# print(names)
	return ids, names

def get_league_name(league_id):
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT name FROM League WHERE id=?
	'''
	name = cur.execute(statement, (league_id,)).fetchone()[0]
	return name

def get_teams(season, league_id):
	global current_season
	current_season = season
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT DISTINCT M.home_team_api_id, T.team_long_name, T.team_short_name
		FROM Match M
			JOIN Team T ON M.home_team_api_id = T.team_api_id
		WHERE M.season=? AND M.league_id=?
		ORDER BY T.team_long_name
	'''
	cur.execute(statement, (season, league_id,))
	ids = []
	names_long = []
	names_short = []
	for row in cur:
		ids.append(row[0])
		names_long.append(row[1])
		names_short.append(row[2])
	conn.close()
	return ids, names_long, names_short

def get_team_name(team_id):
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT team_long_name, team_short_name
		FROM Team
		WHERE team_api_id=?
	'''
	result = cur.execute(statement, (team_id,)).fetchall()[0]
	conn.close()
	return result


def get_all_teams(season):
	global current_season
	current_season = season
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT DISTINCT M.home_team_api_id, T.team_long_name, T.team_short_name
		FROM Match M
			JOIN Team T ON M.home_team_api_id = T.team_api_id
		WHERE M.season=?
		ORDER BY T.team_long_name
	'''
	cur.execute(statement, (season,))
	ids = []
	names_long = []
	names_short = []
	for row in cur:
		ids.append(row[0])
		names_long.append(row[1])
		names_short.append(row[2])
	conn.close()
	return ids, names_long, names_short

def get_team_detail(team_id):
	global current_season
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT buildUpPlaySpeed, buildUpPlayPassing, chanceCreationPassing, chanceCreationCrossing, 
		chanceCreationShooting, defencePressure, defenceAggression, defenceTeamWidth
		FROM Team_Attributes
		WHERE team_api_id=?
		ORDER BY date
		LIMIT 1
	'''
	result = cur.execute(statement, (team_id,)).fetchall()
	conn.close()
	return result

def get_team_word_detail(team_id):
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT buildUpPlayDribblingClass, buildUpPlayPositioningClass, chanceCreationPositioningClass,
		defenceDefenderLineClass
		FROM Team_Attributes
		WHERE team_api_id=?
		ORDER BY date
		LIMIT 1
	'''
	result = cur.execute(statement, (team_id,)).fetchall()
	conn.close()
	return result

def draw_team(data):
	data_list = []
	for d in data[0]:
		data_list.append(d)
	data_list.append(data_list[0])
	data = [go.Scatterpolar(
	  r = data_list,
	  theta = ['Play Speed','Play Passing','Chance-Creation Passing', 'Chance-Creation Crossing', 
	  'Chance-Creation Shooting', 'Defence Pressure', 'Defence Aggression', 'Defence Team Width', 'Play Speed'],
	  fill = 'toself'
	)]

	layout = go.Layout(
	  polar = dict(
	    radialaxis = dict(
	      visible = True,
	      range = [0, 100]
	    )
	  ),
	  showlegend = False,
	  paper_bgcolor='#D2FDFF',
      plot_bgcolor='#D2FDFF'
	)

	fig = go.Figure(data=data, layout=layout)
	div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True, image_width=200, image_height=200)
	return div

def process_records(records):
	plotly_feed_y_data = []
	plotly_feed_x_data = []
	wins = 0
	ties = 0
	loses = 0
	for r in records:
		plotly_feed_x_data.append(r[0])
		if r[1] > r[2]:
			plotly_feed_y_data.append(3)
			wins += 1
		elif r[1] == r[2]:
			plotly_feed_y_data.append(1)
			ties += 1
		else:
			plotly_feed_y_data.append(0)
			loses += 1
	return plotly_feed_x_data, plotly_feed_y_data, wins, ties, loses

def get_match_home_records(team_id):
	global current_season
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT date, home_team_goal, away_team_goal
		FROM Match
		WHERE season=? AND home_team_api_id=?
		ORDER BY date
	'''
	result = cur.execute(statement, (current_season, team_id,)).fetchall()
	conn.close()
	return process_records(result)

def get_match_away_records(team_id):
	global current_season
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT date, away_team_goal, home_team_goal
		FROM Match
		WHERE season=? AND away_team_api_id=?
		ORDER BY date
	'''
	result = cur.execute(statement, (current_season, team_id,)).fetchall()
	conn.close()
	return process_records(result)

def draw_team_records(x_data, y_data, title):
	labels = ['win', 'tie', 'lose']
	tickvals = [3, 1, 0]
	trace = go.Scatter(
	    x = x_data,
	    y = y_data,
	    mode = 'lines+markers',
	    name = 'lines+markers'
	)
	layout = go.Layout(
		yaxis=go.layout.YAxis(
        ticktext=labels,
        tickvals=tickvals
    	),
    	paper_bgcolor='#D2FDFF',
      	plot_bgcolor='#D2FDFF', 
      	title=title,
	)
	data = [trace]
	fig = dict(data=data, layout=layout)
	div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True, image_width=200, image_height=50)
	return div

def get_unique_player(player_tuple1, player_tuple2):
	player_list = []
	for item in player_tuple1:
		for i in item:
			if i and i not in player_list:
				player_list.append(i)
	for item in player_tuple2:
		for i in item:
			if i and i not in player_list:
				player_list.append(i)
	return player_list

def get_squad(team_id):
	global current_season
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT DISTINCT home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11
		FROM Match
		WHERE season=? AND home_team_api_id=?
		ORDER BY date
	'''
	result_home = cur.execute(statement, (current_season, team_id,)).fetchall()
	statement = '''
		SELECT DISTINCT away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11
		FROM Match
		WHERE season=? AND away_team_api_id=?
		ORDER BY date
	'''
	result_away = cur.execute(statement, (current_season, team_id,)).fetchall()
	# print(result_home.extend(result_away))
	player_list = get_unique_player(result_home, result_away)
	conn.close()
	return player_list

def draw_age(ages):
	young = 0
	golden = 0
	retiring = 0
	for a in ages:
		if a < 24:
			young += 1
		elif a > 32:
			retiring += 1
		else:
			golden += 1
	labels = ['Young players (< 24)', 'Golden age players (24 ~ 32)', 'Retiring players (> 32)']
	values = [young, golden, retiring]
	colors = ['#D0F9B1', '#FEBFB3', '#E1396C']
	trace = go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value', 
               textfont=dict(size=20),
               marker=dict(colors=colors, 
                           line=dict(color='#000000', width=2)))
	layout = go.Layout(
    	paper_bgcolor='#D2FDFF',
      	plot_bgcolor='#D2FDFF', 
      	title='Squad Age Formation',
	)
	fig = dict(data=[trace], layout=layout)
	div = plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=True, image_width=200, image_height=50)
	return div

def get_squad_players(team_id):
	global current_season
	player_list = get_squad(team_id)
	player_objs = []
	player_names = []
	player_ids = []
	player_ages = []
	for p in player_list:
		player_objs.append(Player(p))
	for p in player_objs:
		player_names.append(p.get_name())
		player_ids.append(p.player_id)
		player_ages.append(p.get_age())
	fig = draw_age(player_ages)
	return player_ids, player_names, fig

def get_current_season():
	global current_season
	return current_season

def get_player_examples():
	conn = sqlite.connect('database.sqlite')
	cur = conn.cursor()
	statement = '''
		SELECT DISTINCT player_api_id, player_name FROM Player
		ORDER BY player_name
		LIMIT 100
	'''
	result = cur.execute(statement).fetchall()
	player_ids = []
	player_names = []
	for r in result:
		player_ids.append(r[0])
		player_names.append(r[1])
	conn.close()
	return player_ids, player_names

