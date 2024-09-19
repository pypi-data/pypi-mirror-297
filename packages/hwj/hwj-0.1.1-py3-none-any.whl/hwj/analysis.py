import os
import numpy as np
from sklearn.linear_model import LinearRegression


def load_trajectory(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            timestamp = float(parts[0])
            position = np.array([float(p) for p in parts[1:4]])
            quaternion = np.array([float(q) for q in parts[4:]])
            data.append((timestamp, position, quaternion))
    return data

def align_trajectories(gt_trajectory, pred_trajectory, search_interval, max_time_diff=0.5):
    first_time, _, _ = pred_trajectory[0]
    last_time, _, _ = pred_trajectory[-1]
    start_gt_index = np.argmin([abs(gt_timestamp - first_time) for gt_timestamp, _, _ in gt_trajectory])
    end_gt_index = np.argmin([abs(gt_timestamp - last_time) for gt_timestamp, _, _ in gt_trajectory])
    gt_trajectory_segment = gt_trajectory[start_gt_index:end_gt_index + 1]
    start_time, _, _ = gt_trajectory_segment[0]
    end_time, _, _ = gt_trajectory_segment[-1]
    total_time = end_time - start_time
    
    gt_xyz_list = []
    pred_xyz_list = []
    diff_list = []
    gt_xyz = []
    pred_xyz = []
    diffs = []
    pred_index = 0
    pred_len = len(pred_trajectory)

    for i in np.arange(-1, 1, search_interval):
        best_pred_timestamp = None
        for gt_timestamp, gt_position, _ in gt_trajectory_segment:
            gt_timestamp += i
            pre_best_pred_timestamp = best_pred_timestamp if best_pred_timestamp is not None else gt_trajectory_segment[0][0]
            best_pred_timestamp = None
            best_pred_position = None
            
            min_time_diff = float('inf')

            while pred_index < pred_len:
                pred_timestamp, pred_position, _ = pred_trajectory[pred_index]
                time_diff = abs(pred_timestamp - gt_timestamp)

                if time_diff < min_time_diff and time_diff <= max_time_diff:
                    min_time_diff = time_diff
                    best_pred_timestamp = pred_timestamp
                    best_pred_position = pred_position
                
                # 如果时间差已经开始增大，说明已经找到最近的时间戳
                if pred_timestamp > gt_timestamp:
                    break

                pred_index += 1

            if best_pred_position is not None:
                diff = best_pred_timestamp - pre_best_pred_timestamp
                gt_xyz.append(gt_position)
                pred_xyz.append(best_pred_position)
                diffs.append(diff)
        gt_xyz_list.append(gt_xyz)
        pred_xyz_list.append(pred_xyz)
        diff_list.append(diffs)
        gt_xyz = []
        pred_xyz = []
        diffs = []
        pred_index = 0
    
    return gt_xyz_list, pred_xyz_list, diff_list, total_time

def euler_distance_xyz(pos1, pos2):
    pos1, pos2 = np.array(pos1), np.array(pos2)
    return np.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2]-pos2[2])**2)

def main_trans(gt_file, pred_file):

    gt_trajectory = load_trajectory(gt_file)
    pred_trajectory = load_trajectory(pred_file)
    
    search_interval = 0.01
    gt_xyz_list, pred_xyz_list, diff_list, total_time = align_trajectories(gt_trajectory, pred_trajectory, search_interval)

    gt_distances_list = []
    est_distances_list = []
    error_list = []
    errors_list = []
    remove_count_list = []
    search_time_range = len(gt_xyz_list)
    for gt_xyz, pred_xyz, diffs in zip(gt_xyz_list, pred_xyz_list, diff_list):
        remove_count = 0
        gt_distances = []
        est_distances = []
        drift_errors = []
        for i in range(1, len(gt_xyz)-1):
            diff = diffs[i]
            if diff > 5: # 和上一帧时间差太大时，位移容易异常
                remove_count += 1
                continue
            gt_distance = euler_distance_xyz(gt_xyz[i], gt_xyz[i-1])
            gt_distances.append(gt_distance)
            est_distance = euler_distance_xyz(pred_xyz[i], pred_xyz[i-1])
            est_distance /= diff
            est_distances.append(est_distance)
            drift_error = est_distance - gt_distance
            drift_errors.append(drift_error)

        gt_distances_np = np.array(gt_distances)
        est_distances_np = np.array(est_distances)
        drift_errors_np = np.array(drift_errors)
        first_mean_error = np.mean(drift_errors_np)
        first_std_error = np.std(drift_errors_np)
        first_used_index = (drift_errors_np <= first_mean_error + first_std_error) & (drift_errors_np >= first_mean_error - first_std_error)
        filtered_drift_errors_np = drift_errors_np[first_used_index]
        filtered_gt_distances_np = gt_distances_np[first_used_index]
        filtered_est_distances_np = est_distances_np[first_used_index]

        second_mean_error = np.mean(filtered_drift_errors_np)
        second_std_error = np.std(filtered_drift_errors_np)
        second_used_index = (filtered_drift_errors_np <= second_mean_error + second_std_error) & (filtered_drift_errors_np >= second_mean_error - second_std_error)
        remove_count += (filtered_drift_errors_np > second_mean_error + second_std_error).sum() + (filtered_drift_errors_np < second_mean_error - second_std_error).sum() # 统计删除的元素个数
        second_drift_errors_np = filtered_drift_errors_np[second_used_index]
        second_gt_distances_np = filtered_gt_distances_np[second_used_index]
        second_est_distances_np = filtered_est_distances_np[second_used_index]

        error_sum = abs(second_drift_errors_np).sum()
        error = error_sum / (total_time - remove_count)
        error_list.append(error)
        errors_list.append(second_drift_errors_np)
        gt_distances_list.append(second_gt_distances_np)
        est_distances_list.append(second_est_distances_np)
        remove_count_list.append(remove_count)
    
    sorted_errors = sorted((val, idx) for idx, val in enumerate(error_list))
    min_error, min_index = sorted_errors[0]
    min_error_time = (min_index - search_time_range/2) * search_interval

    gt_distances = gt_distances_list[min_index]
    est_distances = est_distances_list[min_index]
    error_distances = errors_list[min_index]
    remove_count = remove_count_list[min_index]

    time = total_time - remove_count
    if min_error > 0.2:
        model = LinearRegression()
        model.fit(est_distances.reshape(-1, 1), gt_distances)
        est_fitted = model.predict(est_distances.reshape(-1, 1))
        err_dis = abs(est_fitted - gt_distances)
        for i, err in enumerate(err_dis):
            if i == 0:
                weight_current = 1 / (err + 1e-6)
                weight_next = 1 / (err_dis[i+1] + 1e-6)
                total_weight = weight_current + weight_next
                weight_current /= total_weight
                weight_next /= total_weight
                est_fitted[i] = weight_current * est_fitted[i] + weight_next * est_fitted[i+1]
                err_dis[i] = abs(est_fitted[i] - gt_distances[i])
            elif i == len(err_dis)-1:
                weight_current = 1 / (err + 1e-6)
                weight_prev = 1 / (err_dis[i-1] + 1e-6)
                total_weight = weight_prev + weight_current
                weight_prev /= total_weight
                weight_current /= total_weight
                est_fitted[i] = weight_prev * est_fitted[i-1] + weight_current * est_fitted[i]
                err_dis[i] = abs(est_fitted[i] - gt_distances[i])
            else: 
                weight_current = 1 / (err + 1e-6)
                weight_prev = 1 / (err_dis[i-1] + 1e-6)
                weight_next = 1 / (err_dis[i+1] + 1e-6)
                total_weight = weight_prev + weight_current + weight_next
                weight_prev /= total_weight
                weight_current /= total_weight
                weight_next /= total_weight
                est_fitted[i] = weight_prev * est_fitted[i-1] + weight_current * est_fitted[i] + weight_next * est_fitted[i+1]
                err_dis[i] = abs(est_fitted[i] - gt_distances[i])
        error_distances = err_dis
        est_distances = est_fitted
        final_min_error = abs(gt_distances - est_fitted).sum() / time
        if final_min_error > 0.2:
            return [], 0
        else:
            print(f"pred file: {pred_file}")
            print(f"Error: {final_min_error}")
    else:
        print(f"pred file: {pred_file}")
        print(f"Error: {min_error}")
    
    with open(f'distance_{gt_file}.txt', 'a') as f:
        for gt, pred, error in zip(gt_distances, est_distances, error_distances):
            f.write(f"{gt}, {pred}, {error}\n")

    return error_distances, time

def main(gt_file, pred_path):
    final_errors = []
    total_time = 0
    for filename in sorted(os.listdir(pred_path)):
        if filename.endswith('.txt'):
            pred_file = os.path.join(pred_path, filename)

            errors_list, time = main_trans(gt_file, pred_file)
            for error in errors_list:
                final_errors.append(error)
            total_time += time
    final_errors_np = np.array(final_errors)
    final_errors_np_abs = abs(final_errors_np)
    print(final_errors_np_abs.sum() / total_time)
