import matplotlib.pyplot as plt
import pandas as pd
import pygame

def show_graphs(screen):
    # Load CSV 
    try:
        df = pd.read_csv("game_data.csv")

        # Convert cumulative to per-interval
        df["zombies_killed_elapsed"] = df["zombies_killed"].diff().fillna(df["zombies_killed"])
        df["trash_collected_elapsed"] = df["trash_collected"].diff().fillna(df["trash_collected"])
        df["bullets_fired_elapsed"] = df["bullets_fired"].diff().fillna(df["bullets_fired"])
        df["score_elapsed"] = df["score"].diff().fillna(df["score"])
        df["leftover_elapsed"] = (df["leftover_trash"] + df["alive_zombies"]).diff().fillna(df["leftover_trash"] + df["alive_zombies"])

        # Elimination percentage per interval
        df["total_actions_elapsed"] = df["zombies_killed_elapsed"] + df["trash_collected_elapsed"] + df["leftover_elapsed"]
        df["elimination_pct_elapsed"] = (df["zombies_killed_elapsed"] + df["trash_collected_elapsed"]) / df["total_actions_elapsed"].replace(0, 1) * 100

        # Compute  statistics
        stats_data = {
            "Scores": df["score_elapsed"],
            "Trash Collected": df["trash_collected_elapsed"],
            "Zombies Killed": df["zombies_killed_elapsed"]
        }

        summary = {}
        for key, series in stats_data.items():
            summary[key] = {
                "Range": series.max() - series.min(),
                "Mean": series.mean(),
                "Median": series.median(),
                "Mode": series.mode().iloc[0] if not series.mode().empty else None
            }

        
    except FileNotFoundError:
        screen.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 40)
        text = font.render("No stats available yet!", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2,
                           screen.get_height()//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(2000)
        return

    # Compute elimination percentage
    df["total_actions"] = df["zombies_killed"] + df["trash_collected"] + df["leftover_trash"] + df["alive_zombies"]
    df["elimination_pct"] = (df["zombies_killed"] + df["trash_collected"]) / df["total_actions"].replace(0, 1) * 100

    # Compute points breakdown
    zombie_points = df["zombies_killed"] * 50
    trash_points = df["trash_collected"] * 10

    # Not secretive plotter
    def plot_bar():
        plt.figure(figsize=(8, 6))
        plt.bar(df["elapsed_seconds"], df["zombies_killed_elapsed"], label="Zombies Killed (per 5s)")
        plt.bar(df["elapsed_seconds"], df["trash_collected_elapsed"], bottom=df["zombies_killed_elapsed"], label="Trash Collected (per 5s)")
        plt.bar(df["elapsed_seconds"], df["leftover_elapsed"],
                bottom=df["zombies_killed_elapsed"] + df["trash_collected_elapsed"], label="Leftover (per 5s)")
        plt.title("Bar Graph: Actions per Interval")
        plt.xlabel("Elapsed Seconds")
        plt.ylabel("Count")
        plt.legend()

    def plot_elimination():
        plt.figure(figsize=(8, 6))
        plt.plot(df["elapsed_seconds"], df["elimination_pct_elapsed"], marker="o")
        plt.title("Elimination % per Interval")
        plt.xlabel("Elapsed Seconds")
        plt.ylabel("Elimination %")
        plt.ylim(0, 100)

    def plot_bullets_vs_kills():
        plt.figure(figsize=(8, 6))
        plt.scatter(df["bullets_fired_elapsed"], df["zombies_killed_elapsed"], c="red")
        plt.title("Bullets Fired vs Zombies Killed (per 5s)")
        plt.xlabel("Bullets Fired (per 5s)")
        plt.ylabel("Zombies Killed (per 5s)")

    def plot_points_vs_time():
        plt.figure(figsize=(8, 6))
        plt.plot(df["elapsed_seconds"], df["score_elapsed"], marker="o", color="orange")
        plt.title("Points per Interval vs Time")
        plt.xlabel("Elapsed Seconds")
        plt.ylabel("Points (per 5s)")

    def plot_leftover_vs_elimination():
        plt.figure(figsize=(8, 6))
        plt.scatter(df["leftover_elapsed"], df["elimination_pct_elapsed"], c="green")
        plt.title("Leftover vs Elimination % (per 5s)")
        plt.xlabel("Leftover (per 5s)")
        plt.ylabel("Elimination % (per 5s)")

    def plot_pie_points():
        plt.figure(figsize=(8, 6))
        zombie_points = (df["zombies_killed_elapsed"] * 50).sum()
        trash_points = (df["trash_collected_elapsed"] * 10).sum()
        plt.pie([zombie_points, trash_points],
                labels=["Zombie Points", "Trash Points"],
                autopct="%1.1f%%", colors=["red", "blue"])
        plt.title("Points Collection Breakdown (per 5s)")
    
    def plot_stats_table():
        plt.figure(figsize=(10, 6))   # more space
        plt.axis("off")

        columns = ["Range", "Mean", "Median", "Mode"]
        rows = list(summary.keys())
        cell_text = [[f"{summary[row][col]:.2f}" if summary[row][col] is not None else "N/A"
                    for col in columns] for row in rows]

        table = plt.table(cellText=cell_text,
                        rowLabels=rows,
                        colLabels=columns,
                        loc="center")

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.0, 1.5)   # adjust scaling so it fits

        plt.title("Statistics Summary (Scores, Trash, Zombies)")
        plt.tight_layout()



    # List of graphs
    graphs = [plot_bar, plot_elimination, plot_bullets_vs_kills,
              plot_points_vs_time, plot_leftover_vs_elimination, plot_pie_points, plot_stats_table]

    index = 0
    running = True

    while running:
        plt.close("all")
        graphs[index]()   # draw current graph
        plt.show()
        
        #cant use this, it crashed
        #plt.show(block=False)   
        #plt.pause(0.5)          


        # Instruction overlay in pygame
        screen.fill((30,30,30))
        font = pygame.font.SysFont(None, 30)
        text1 = font.render("SPACE = Next | BACKSPACE = Previous | ESC = Exit", True, (255,255,255))
        text2 = font.render(f"Showing Graph {index+1} of {len(graphs)}", True, (200,200,200))
        screen.blit(text1, (screen.get_width()//2 - text1.get_width()//2, screen.get_height()-60))
        screen.blit(text2, (screen.get_width()//2 - text2.get_width()//2, screen.get_height()-30))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        index = (index + 1) % len(graphs)
                        waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        index = (index - 1) % len(graphs)
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        waiting = False
