import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

class Stats():
    def plot(x_val, players):
        matplotlib.use('agg')
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
        
        # # Avg. turn time per melds in hand
        # axis = ax['lower left']
        # axis.set_title("Avg. turn time in seconds per melds in hand")
        # axis.set_ylabel("Avg. turn time") 
        # axis.set_xlabel("Melds in hand")
        # player_turn_time_per_melds_in_hand_stats = {
        #     f'{players[0].name}': tuple(players[0].get_avg_turn_times_per_meld_cards_in_hand()),
        #     f'{players[1].name}': tuple(players[1].get_avg_turn_times_per_meld_cards_in_hand()),
        # }
        # x = np.arange(len(players[0].get_avg_turn_times_per_meld_cards_in_hand()))  # the label locations
        # width = 0.25  # the width of the bars
        # multiplier = 0
        # for attribute, measurement in player_turn_time_per_melds_in_hand_stats.items():
        #     offset = width * multiplier
        #     if len(x) != len(measurement):
        #         x = np.arange(len(measurement))
        #     rects = axis.bar(x + offset, measurement, width, label=attribute)
        #     #axis.bar_label(rects, padding=3)
        #     multiplier += 1
        # x = np.arange(len(players[0].get_avg_turn_times_per_meld_cards_in_hand()))  # the label locations
        # axis.set_xticks(x + width, tuple(ele for ele in range(0, len(players[0].get_avg_turn_times_per_meld_cards_in_hand()))))
        # axis.legend(loc='upper left', ncols=3)
        # max_p = max(max(players[0].get_avg_turn_times_per_meld_cards_in_hand()), max(players[1].get_avg_turn_times_per_meld_cards_in_hand()))
        # axis.set_ylim(0, max_p * 1.1)
        
        # Table
        axis = ax['right']
        axis.axis('off')
        axis.axis('tight')
        cell_text = []
        cell_text.append(["", players[0].name, players[1].name])
        cell_text.append(["Depth", players[0].depth, players[1].depth])
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
        
        # fig.legend(lines, labels, loc='upper right') 

    def finalize_plot(name_bot1, name_bot2):
        #fig_path = f'stats/stats-{name_bot1}-vs-{name_bot2}-{date.today().strftime("%m-%d-%Y")}.png'
        #plt.savefig(fig_path)
        pass
