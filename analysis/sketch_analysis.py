import csv
import os
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import re

def analyze_drawing(csv_path, visualize=False):
    """Analizza un file CSV e restituisce le metriche e i tratti stimati."""
    times, xs, ys = [], [], []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # delete rows with mouse_pressed == 0
            if int(row["mouse_pressed"]) == 0:
                continue
            times.append(float(row["time"]))
            xs.append(float(row["x"]))
            ys.append(float(row["y"]))

    if len(times) < 2:
        return None

    # --- Parametri ---
    TIME_GAP_THRESHOLD = 0.8   # seconds
    DIST_THRESHOLD = 30        # pixel
    SPEED_SPIKE_FACTOR = 4     # volte la velocità media locale
    MIN_POINTS_PER_STROKE = 5  # ignore micro-touches shorter than 5 points

    velocities, curvatures = [], []
    stroke_indices = [0]
    stroke_count = 1
    total_dist = 0.0

    # --- Total drawing time ---
    if len(times) > 1:
        total_time = times[-1] - times[0]  # time difference in seconds
    else:
        total_time = 0.0


    # loop through points to compute distances, velocities, curvatures, and strokes
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        dx = xs[i] - xs[i - 1]
        dy = ys[i] - ys[i - 1]
        dist = math.hypot(dx, dy)
        total_dist += dist

        # Velocità istantanea
        v = dist / dt if dt > 0 else 0
        velocities.append(v)

        # Curvatura
        if i > 1:
            dx1 = xs[i - 1] - xs[i - 2]
            dy1 = ys[i - 1] - ys[i - 2]
            dx2 = xs[i] - xs[i - 1]
            dy2 = ys[i] - ys[i - 1]
            denom = math.hypot(dx1, dy1) * math.hypot(dx2, dy2)
            if denom > 0:
                cos_angle = (dx1 * dx2 + dy1 * dy2) / denom
                cos_angle = max(-1, min(1, cos_angle))
                curvatures.append(math.acos(cos_angle))

        # --- Stroke counting ---
        if i > 5: # at least 5 previous points to compute local mean velocity
            # compute the local mean velocity using the last 5 velocity samples
            local_mean_v = sum(velocities[-5:]) / 5

            # Check three conditions that each indicate a likely start of a new stroke:
            # 1) a long time gap (pause) since the previous point
            # 2) a large spatial jump since the previous point
            # 3) an unusually high instantaneous speed compared to recent local mean speed
            if (
                # dt > TIME_GAP_THRESHOLD or                     # time gap too large -> likely lift
                # minimum number of points per stroke to avoid noise
                (i - stroke_indices[-1] >= MIN_POINTS_PER_STROKE and
                dist > DIST_THRESHOLD)
                #or                       # spatial jump too large -> likely jump
                # (local_mean_v > 0 and v > SPEED_SPIKE_FACTOR * local_mean_v)  # speed spike -> likely move between regions
            ):
                stroke_count += 1              # increment the estimated number of strokes
                stroke_indices.append(i)       # record the index where a new stroke is considered to start


    mean_vel = np.mean(velocities) # velocity [pixel / sec]
    max_vel = np.max(velocities)
    mean_curv = np.mean(curvatures) if curvatures else 0

    # Dimensioni disegno
    drawing_width = max(xs) - min(xs)
    drawing_height = max(ys) - min(ys)
    
    # trial number extraction
    match = re.search(r"trial_(\d+)([A-Za-z]?)_subj", os.path.basename(csv_path))
    if match:
        number = int(match.group(1))          # parte numerica
        letter = match.group(2)               # eventuale lettera
        trial = f"{number:02d}{letter}"  

    # --- Visualizzazione ---
    if visualize:
        plt.figure(figsize=(8, 8))
        plt.axis("equal")
        plt.title(f"Drawing: {os.path.basename(csv_path)}\nEstimated strokes: {stroke_count}")
        plt.xlabel("x (pixels)")
        plt.ylabel("y (pixels)")

        # Mappa colori
        colors = cm.rainbow(np.linspace(0, 1, stroke_count))

        for s in range(len(stroke_indices)):
            start = stroke_indices[s]
            end = stroke_indices[s + 1] if s + 1 < len(stroke_indices) else len(xs)
            plt.plot(xs[start:end], ys[start:end], color=colors[s], linewidth=3)

        plt.gca().invert_yaxis()  # per avere la stessa direzione di coordinate del canvas
        plt.show()

    return {
        "file": os.path.basename(csv_path),
        "subject": re.search(r"subj_(\d+)_2025", os.path.basename(csv_path)).group(1),
        "trial": trial,
        "strokes": stroke_count,
        "total_distance_px": round(total_dist, 2),
        "mean_velocity_px_s": round(mean_vel, 3),
        "max_velocity_px_s": round(max_vel, 3),
        "mean_curvature_rad": round(mean_curv, 3),
        "drawing_width_px": round(drawing_width, 2),
        "drawing_height_px": round(drawing_height, 2),
        "total_time": round(total_time, 2)
    }


if __name__ == "__main__":
    folder = "drawings/robot/06"
    results = []

    files = os.listdir(folder)
    sorted_files = sorted(files)
    for file in sorted_files:
        if file.endswith(".csv"):
            path = os.path.join(folder, file)
            metrics = analyze_drawing(path, visualize=False)
            if metrics:
                results.append(metrics)
                print(metrics)
    # Salva i risultati complessivi in un file CSV
    keys = results[0].keys()
    with open("analysis/robot/06.csv", "w", newline="") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
        print("Summary saved to drawing_metrics_summary.csv")
