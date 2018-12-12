from flask import Flask, render_template, request, redirect
import model

app = Flask(__name__)

@app.route("/")
def index():
	seasons = model.get_seasons()
	league_ids, league_names = model.get_leagues()
	return render_template("index.html", seasons=seasons, league_ids=league_ids, 
		league_names=league_names, league_num=len(league_ids))

@app.route("/showteams", methods=["POST"])
def show_teams():
	season = request.form["seasonList"]
	league_id = request.form["leagueList"]
	league_name = model.get_league_name(league_id)
	ids, names_long, names_short = model.get_teams(season, int(league_id))
	return render_template("showteams.html", ids=ids, names_long=names_long, 
		names_short=names_short, league_name=league_name, season=season, team_num=len(ids))

@app.route('/teams/<team_id>')
def show_team_detail(team_id):
	name_long = model.get_team_name(team_id)[0]
	name_short = model.get_team_name(team_id)[1]
	details = model.get_team_detail(team_id)
	details_fig = model.draw_team(details)
	word_details = model.get_team_word_detail(team_id)
	plotly_feed_x_data_home, plotly_feed_y_data_home, wins_home, ties_home, loses_home = model.get_match_home_records(team_id)
	plotly_feed_x_data_away, plotly_feed_y_data_away, wins_away, ties_away, loses_away = model.get_match_away_records(team_id)
	record_fig_home = model.draw_team_records(plotly_feed_x_data_home, plotly_feed_y_data_home, 'As Home Team')
	record_fig_away = model.draw_team_records(plotly_feed_x_data_away, plotly_feed_y_data_away, 'As Away Team')
	player_ids, player_names, age_fig = model.get_squad_players(team_id)
	season = model.get_current_season()
	return render_template("teamdetail.html", name_long=name_long, name_short=name_short, 
		details_fig=details_fig, word_details=word_details, details=details, 
		record_fig_home=record_fig_home, record_fig_away=record_fig_away, 
		wins_home=wins_home, ties_home=ties_home, loses_home=loses_home,
		wins_away=wins_away, ties_away=ties_away, loses_away=loses_away,
		win_percentage_home=round(wins_home/(wins_home+ties_home+loses_home)*100),
		win_percentage_away=round(wins_away/(wins_away+ties_away+loses_away)*100),
		win_percentage_total=round((wins_away+wins_home)/(wins_away+ties_away+loses_away+wins_home+ties_home+loses_home)*100),
		player_ids=player_ids, player_names=player_names, age_fig=age_fig, player_num=len(player_ids),
		season=season)

@app.route("/allteams", methods=["GET", "POST"])
def show_all_teams():
	seasons = model.get_seasons()
	try:
		select_season = request.form["seasonList"]
		ids, names_long, names_short = model.get_all_teams(select_season)
		team_num = len(ids)
	except:
		select_season = None
		ids = None
		names_long = None
		names_short = None
		team_num = None
	return render_template("allteams.html", ids=ids, names_long=names_long, 
		names_short=names_short, select_season=select_season, team_num=team_num, seasons=seasons)

@app.route('/player/<player_id>')
def show_player_detail(player_id):
	player = model.Player(player_id)
	general_info = player.get_general_info()
	height = general_info[0]
	weight = general_info[1]
	name = player.get_name()
	age = player.get_age()
	general_attr = player.get_general_attr()
	attack_fig = player.get_attack_attr()
	skill_fig = player.get_skill_attr()
	move_fig = player.get_move_attr()
	power_fig = player.get_power_attr()
	ment_fig = player.get_ment_attr()
	def_fig = player.get_def_attr()
	gk_fig = player.get_gk_attr()
	return render_template("playerdetail.html", height=height, weight=weight, name=name, 
		age=age, general_attr=general_attr, attack_fig=attack_fig, skill_fig=skill_fig, 
		move_fig=move_fig, power_fig=power_fig, ment_fig=ment_fig, def_fig=def_fig, 
		gk_fig=gk_fig)

@app.route("/allplayers", methods=["GET", "POST"])
def show_all_players():
	player_ids, player_names = model.get_player_examples()
	return render_template("allplayers.html", ids=player_ids, names=player_names, num=len(player_ids))

if __name__=="__main__":
	app.run(debug=True)