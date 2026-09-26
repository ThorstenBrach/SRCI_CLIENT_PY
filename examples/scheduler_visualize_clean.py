"""
Scheduler with Visualization - OPTIMIZED
"""

from RobotLibrary.IEC_Scheduler import Task, Scheduler, TaskType, TaskPriority
import time
import matplotlib.pyplot as plt
from collections import deque
import threading


class LockFreeHistory:
    def __init__(self, maxlen=50000):  # Increased for 30s @ 1ms interval = 30000 entries
        self.execution_times = deque(maxlen=maxlen)
        self.timestamps = deque(maxlen=maxlen)
        self.start_times = deque(maxlen=maxlen)
        self.end_times = deque(maxlen=maxlen)
        self.lock = threading.Lock()
    
    def append(self, exec_time, timestamp, start_time, end_time):
        with self.lock:
            self.execution_times.append(exec_time)
            self.timestamps.append(timestamp)
            self.start_times.append(start_time)
            self.end_times.append(end_time)
    
    def get_snapshot(self):
        with self.lock:
            return (list(self.execution_times), list(self.timestamps), 
                   list(self.start_times), list(self.end_times))


task_histories = {
    'Fast': LockFreeHistory(),
    'Medium': LockFreeHistory(),
    'Slow': LockFreeHistory()
}

start_time = None


def create_wrapper(task_name: str, original_function):
    history = task_histories[task_name]
    
    def wrapper():
        exec_start = time.perf_counter()
        original_function()
        exec_end = time.perf_counter()
        exec_time = exec_end - exec_start
        timestamp = exec_end - start_time
        start_rel = exec_start - start_time
        end_rel = exec_end - start_time
        history.append(exec_time * 1000.0, timestamp, start_rel, end_rel)
    
    return wrapper


def fast_task():
    result = 0.0
    for i in range(10000):
        result += i ** 0.5


def medium_task():
    result = 0.0
    for i in range(50000):
        result += i ** 0.5


def slow_task():
    result = 0.0
    for i in range(100000):
        result += i ** 0.5


def plot_visualizations():
    """Shows 3 separate windows with visualizations"""
    colors = {'Fast': 'blue', 'Medium': 'green', 'Slow': 'red'}
    task_names = ['Fast', 'Medium', 'Slow']
    
    # Collect data
    all_data = {}
    print("\n" + "="*80)
    print("DATA COLLECTION CHECK:")
    print("="*80)
    for task_name in task_names:
        exec_times, timestamps, start_times, end_times = task_histories[task_name].get_snapshot()
        all_data[task_name] = (exec_times, timestamps, start_times, end_times)
        print(f"\n{task_name}:")
        print(f"  Total Entries: {len(start_times)}")
        if start_times:
            time_span = max(start_times) - min(start_times)
            print(f"  Time Range: {min(start_times):.6f}s to {max(start_times):.6f}s (span: {time_span:.3f}s)")
            print(f"  First 5 starts: {[f'{s:.6f}' for s in start_times[:5]]}")
            print(f"  Last 5 starts: {[f'{s:.6f}' for s in start_times[-5:]]}")
            print(f"  Average interval: {time_span / (len(start_times)-1) * 1000:.3f}ms" if len(start_times) > 1 else "  N/A")
        else:
            print(f"  WARNING: NO DATA CAPTURED!")
    print("="*80)
    
    # === WINDOW 1: TIMELINE ===
    from matplotlib.widgets import SpanSelector
    import matplotlib.patches as mpatches
    
    fig1 = plt.figure(figsize=(18, 10))
    fig1.canvas.manager.set_window_title('Timeline')
    
    gs1 = fig1.add_gridspec(2, 1, height_ratios=[3, 0.5], hspace=0.25)
    ax_main = fig1.add_subplot(gs1[0])
    ax_info = fig1.add_subplot(gs1[1])
    ax_info.axis('off')
    
    y_positions = {'Fast': 0.2, 'Medium': 0.1, 'Slow': 0}
    max_time = max([max(all_data[tn][2]) if all_data[tn][2] else 0 for tn in task_names])
    view_max = min(5.0, max_time + 0.1) if max_time > 0 else 5.0
    
    def draw_timeline(t_min, t_max):
        ax_main.clear()
        
        for task_name in task_names:
            _, _, starts, ends = all_data[task_name]
            y = y_positions[task_name]
            color = colors[task_name]
            
            count = 0
            for start, end in zip(starts, ends):
                if t_min <= start <= t_max:
                    if task_name == 'Fast':
                        # Vertical span for Fast
                        ax_main.axvspan(start, end, ymin=(y-0.04)/0.3+0.03, ymax=(y+0.04)/0.3+0.03,
                                      color=color, alpha=0.8, linewidth=0)
                    else:
                        # Bars for Medium/Slow
                        ax_main.barh(y, end-start, left=start, height=0.08,
                                   color=color, alpha=0.7, edgecolor='black', linewidth=0.8)
                    count += 1
            
            if count > 0:
                ax_main.text(t_max * 0.98, y, f'n={count}', fontsize=11, ha='right', va='center',
                           weight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow'))
        
        ax_main.set_yticks([0, 0.1, 0.2])
        ax_main.set_yticklabels(task_names[::-1], fontsize=12, weight='bold')
        ax_main.set_xlabel('Time (s)', fontsize=11)
        ax_main.set_ylabel('Task', fontsize=11)
        ax_main.set_xlim(t_min, t_max)
        ax_main.set_ylim(-0.05, 0.28)
        ax_main.grid(True, alpha=0.4, axis='x')
        ax_main.set_title('Task Timeline', fontsize=13, weight='bold')
        
        legend_elements = [mpatches.Patch(facecolor=colors[tn], alpha=0.7, label=tn) for tn in task_names]
        ax_main.legend(handles=legend_elements, loc='upper left')
    
    draw_timeline(0, view_max)
    
    # Cursors
    cursor_positions = [view_max * 0.3, view_max * 0.7]
    cursor_lines = [
        ax_main.axvline(cursor_positions[0], color='red', linewidth=2.5, linestyle='--', alpha=0.9, zorder=100),
        ax_main.axvline(cursor_positions[1], color='magenta', linewidth=2.5, linestyle='--', alpha=0.9, zorder=100)
    ]
    active_cursor = [None]
    
    distance_text = ax_info.text(0.5, 0.5, '', transform=ax_info.transAxes, fontsize=13, weight='bold',
                                ha='center', va='center', bbox=dict(boxstyle='round,pad=0.8',
                                facecolor='lightyellow', edgecolor='black', linewidth=2))
    
    def update_distance():
        pos1_ms = cursor_positions[0] * 1000
        pos2_ms = cursor_positions[1] * 1000
        dist_ms = abs(cursor_positions[1] - cursor_positions[0]) * 1000
        distance_text.set_text(f'C1: {pos1_ms:.3f}ms | C2: {pos2_ms:.3f}ms | Δt: {dist_ms:.3f}ms')
    
    update_distance()
    
    def on_select(xmin, xmax):
        draw_timeline(xmin, xmax)
        cursor_lines[0] = ax_main.axvline(cursor_positions[0], color='red', linewidth=2.5,
                                         linestyle='--', alpha=0.9, zorder=100)
        cursor_lines[1] = ax_main.axvline(cursor_positions[1], color='magenta', linewidth=2.5,
                                         linestyle='--', alpha=0.9, zorder=100)
        fig1.canvas.draw_idle()
    
    def on_press(event):
        if event.inaxes != ax_main or event.xdata is None:
            return
        distances = [abs(event.xdata - pos) for pos in cursor_positions]
        active_cursor[0] = distances.index(min(distances))
    
    def on_move(event):
        if active_cursor[0] is None or event.inaxes != ax_main or event.xdata is None:
            return
        cursor_positions[active_cursor[0]] = event.xdata
        cursor_lines[active_cursor[0]].set_xdata([event.xdata])
        update_distance()
        fig1.canvas.draw_idle()
    
    def on_release(event):
        active_cursor[0] = None
    
    SpanSelector(ax_main, on_select, 'horizontal', useblit=True,
                props=dict(alpha=0.25, facecolor='orange'), interactive=True, drag_from_anywhere=True)
    
    fig1.canvas.mpl_connect('button_press_event', on_press)
    fig1.canvas.mpl_connect('motion_notify_event', on_move)
    fig1.canvas.mpl_connect('button_release_event', on_release)
    
    # === WINDOW 2: EXECUTION TIMES ===
    fig2, axes = plt.subplots(3, 1, figsize=(16, 10))
    fig2.canvas.manager.set_window_title('Execution Times')
    
    for idx, task_name in enumerate(task_names):
        ax = axes[idx]
        exec_times, times, _, _ = all_data[task_name]
        
        if not exec_times:
            continue
        
        ax.scatter(times, exec_times, alpha=0.3, s=1, color=colors[task_name])
        
        if len(exec_times) > 100:
            window = 100
            moving_avg = [sum(exec_times[i:i+window])/window 
                         for i in range(0, len(exec_times)-window, 10)]
            moving_times = [times[i+window//2] for i in range(0, len(exec_times)-window, 10)]
            ax.plot(moving_times, moving_avg, color=colors[task_name], linewidth=2)
        
        import statistics
        median = statistics.median(exec_times)
        p95 = sorted(exec_times)[int(len(exec_times) * 0.95)]
        
        ax.axhline(y=median, color='orange', linestyle='--', linewidth=1, alpha=0.7, label=f'Median: {median:.2f}ms')
        ax.axhline(y=p95, color='red', linestyle=':', linewidth=1, alpha=0.7, label=f'95th: {p95:.2f}ms')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Execution Time (ms)')
        ax.set_title(f'{task_name}')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    
    # === WINDOW 3: STATISTICS ===
    fig3, axes3 = plt.subplots(2, 1, figsize=(14, 8))
    fig3.canvas.manager.set_window_title('Statistics')
    
    ax1 = axes3[0]
    for task_name in task_names:
        exec_times, times, _, _ = all_data[task_name]
        if exec_times and len(exec_times) > 100:
            window = 100
            moving_avg = [sum(exec_times[i:i+window])/window 
                         for i in range(0, len(exec_times)-window, 20)]
            moving_times = [times[i+window//2] for i in range(0, len(exec_times)-window, 20)]
            ax1.plot(moving_times, moving_avg, label=f'{task_name}', color=colors[task_name], linewidth=2)
    
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Execution Time (ms)')
    ax1.set_title('Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes3[1]
    data_for_box = []
    labels_for_box = []
    for task_name in task_names:
        exec_times, _, _, _ = all_data[task_name]
        if exec_times:
            data_for_box.append(exec_times)
            labels_for_box.append(task_name)
    
    bp = ax2.boxplot(data_for_box, tick_labels=labels_for_box, patch_artist=True, showfliers=True)
    for patch, task_name in zip(bp['boxes'], labels_for_box):
        patch.set_facecolor(colors[task_name])
        patch.set_alpha(0.6)
    
    ax2.set_ylabel('Execution Time (ms)')
    ax2.set_title('Distribution')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()


def print_statistics():
    print("\n" + "="*100)
    print("Detailed Execution Time Statistics:")
    print("="*100)
    print(f"{'Task':<15} {'Count':<10} {'Min(ms)':<10} {'Median(ms)':<12} {'Avg(ms)':<10} "
          f"{'95th(ms)':<10} {'Max(ms)':<10} {'StdDev(ms)':<12} {'Jitter(ms)':<12}") 
    print("-"*100)
    
    for task_name in ['Fast', 'Medium', 'Slow']:
        exec_times, _, _, _ = task_histories[task_name].get_snapshot()
        
        if exec_times:
            import statistics
            count = len(exec_times)
            min_time = min(exec_times)
            max_time = max(exec_times)
            avg_time = sum(exec_times) / count
            median_time = statistics.median(exec_times)
            std_dev = statistics.stdev(exec_times) if count > 1 else 0.0
            p95 = sorted(exec_times)[int(count * 0.95)]
            jitter = max_time - min_time
            
            print(f"{task_name:<15} {count:<10} {min_time:<10.3f} {median_time:<12.3f} {avg_time:<10.3f} "
                  f"{p95:<10.3f} {max_time:<10.3f} {std_dev:<12.3f} {jitter:<12.3f}")
    
    print("="*100)


if __name__ == "__main__":
    print("Task Scheduler with Visualization")
    print("Runtime: 30 seconds")
    print("-" * 80)
    
    start_time = time.perf_counter()
    scheduler = Scheduler()
    
    scheduler.add_task(Task(
        name="Fast",
        function=create_wrapper("Fast", fast_task),
        task_type=TaskType.CYCLIC,
        interval_ms=1,
        priority=TaskPriority.HIGH,
        watchdog_ms=0,
        autostart=True
    ))
    
    scheduler.add_task(Task(
        name="Medium",
        function=create_wrapper("Medium", medium_task),
        task_type=TaskType.CYCLIC,
        interval_ms=5,
        priority=TaskPriority.NORMAL,
        watchdog_ms=0,
        autostart=True
    ))
    
    scheduler.add_task(Task(
        name="Slow",
        function=create_wrapper("Slow", slow_task),
        task_type=TaskType.CYCLIC,
        interval_ms=10,
        priority=TaskPriority.LOW,
        watchdog_ms=0,
        autostart=True
    ))
    
    print("\nTasks running... (30s)")
    print("Checking data collection every 5s...\n")
    
    for i in range(6):
        time.sleep(5.0)
        for task_name in ['Fast', 'Medium', 'Slow']:
            _, _, starts, _ = task_histories[task_name].get_snapshot()
            print(f"  [{i*5:2d}s] {task_name}: {len(starts)} entries")
    
    scheduler.stop_all()
    
    print("\n>>> Scheduler Status:")
    scheduler.print_status()
    
    print_statistics()
    
    print("\nCreating visualizations...")
    plot_visualizations()
    
    print("\nDone!")
