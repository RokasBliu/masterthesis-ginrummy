import matplotlib.pyplot as plt
import numpy as np

class Stats():
    def plot(x_val, players):
        # Create plot
        # fig, ax = plt.subplots(nrows=2, ncols=1, squeeze=False)
        gs_kw = dict(width_ratios=[1, 1], height_ratios=[1, 1])
        fig, ax = plt.subplot_mosaic([['upper left', 'right'],
                               ['lower left', 'right']],
                              gridspec_kw=gs_kw, figsize=(7.5, 7.5),
                              layout="constrained")
        x = x_val
        if type(x_val) is int:
            x = np.linspace(0, x, x)

        # Score per game plot
        axis = ax['upper left']
        axis.set_title("Score per game")
        axis.set_ylabel("Score")
        axis.set_xlabel("Game Nr.")
        max_score = 0
        for player in players:
            temp_max = max(player.score_per_game)
            if temp_max > max_score:
                max_score = temp_max
            axis.plot(x, player.score_per_game, linewidth=2.0)
        axis.set(xlim=(0, x_val), xticks=np.arange(0, x_val+1, 20),
            ylim=(0, max_score), yticks=np.arange(0, max_score, 20))
        
        # Wins per game plot
        axis = ax['lower left']
        axis.set_title("Wins per game")
        axis.set_ylabel("Wins") 
        axis.set_xlabel("Games")
        for player in players:
            axis.plot(x, player.wins_per_game, linewidth=2.0)
        axis.set(xlim=(0, x_val), xticks=np.arange(0, x_val+1, 20),
            ylim=(0, x_val), yticks=np.arange(0, x_val+1, 10))
        
        # Table
        axis = ax['right']
        axis.axis('off')
        axis.axis('tight')
        cell_text = []
        cell_text.append(["", players[0].name, players[1].name])
        cell_text.append(["Winrate", players[0].get_winrate(), players[1].get_winrate()])
        cell_text.append(["Wins", players[0].wins, players[1].wins])
        cell_text.append(["Round wins", players[0].get_total_round_wins(), players[1].get_total_round_wins()])
        cell_text.append(["Avg. score\npr. game", players[0].get_avg_score_per_game(), players[1].get_avg_score_per_game()])
        cell_text.append(["Avg. score\npr. round", players[0].get_avg_score_per_round(), players[1].get_avg_score_per_round()])
        cell_text.append(["Undercuts", players[0].total_undercuts, players[1].total_undercuts])
        cell_text.append(["Gins", players[0].total_gins, players[1].total_gins])
        cell_text.append(["Knocks", players[0].total_knocks, players[1].total_knocks])
        cell_text.append(["Avg. draw\ntime (sec)", players[0].get_avg_draw_time(), players[1].get_avg_draw_time()])
        cell_text.append(["Avg. discard\n time (sec)", players[0].get_avg_discard_time(), players[1].get_avg_discard_time()])
        # table = axis.table(cellText=cell_text, rowLabels=rows, colLabels=columns, loc='center')
        table = axis.table(cellText=cell_text, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1,4)
        fig.tight_layout()

        lines = [] 
        labels = []
        for ax in fig.axes: 
            Line, Label = ax.get_legend_handles_labels() 
            lines.extend(Line) 
            labels.extend(Label) 
        
        fig.legend(lines, labels, loc='upper right') 

    def finalize_plot():
        plt.savefig('stats.png')