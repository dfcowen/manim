from manim import *
import h5py
import numpy as np
from collections import defaultdict

class DetectorVisualization(ThreeDScene):
    def __init__(self, NEvents=1, DebugPrint=True):
        super().__init__()
        self.NEvents = NEvents
        self.module_positions = {}
        self.events_to_process = []
        self.DebugPrint = DebugPrint
        
    def load_geometry(self):
        if self.DebugPrint: print("Opening geometry file...")
        with h5py.File('GeoCalibDetectorStatus_AVG_55697-57531_PASS2_SPE_withScaledNoise.hdf5', 'r') as f:
            if self.DebugPrint: print("Reading geometry data...")
            geo_data = np.array(f['geo'])
            labels = np.array([label.decode('utf-8') for label in f['labels']])
            if self.DebugPrint: print("Creating column indices...")
            col_indices = {label: idx for idx, label in enumerate(labels)}
            
            if self.DebugPrint: print("Processing geometry rows...")
            for row in geo_data:
                string = int(row[col_indices['string']])
                om = int(row[col_indices['om']])
                pos = (float(row[col_indices['pos_x']]),
                      float(row[col_indices['pos_y']]),
                      float(row[col_indices['pos_z']]))
                self.module_positions[(string, om)] = pos

    def get_event_list(self, filename):
        if self.DebugPrint: print(f"Opening {filename} for event list...")
        with h5py.File(filename, 'r') as f:
            if self.DebugPrint: print("Reading hit data...")
            hits = np.array(f['SRTTWOfflinePulsesDC'])
            if self.DebugPrint: print("Finding unique events...")
            unique_events = np.unique(hits[['Run', 'Event']])
            return unique_events[:self.NEvents]

    def process_event(self, filename, target_run, target_event):
        if self.DebugPrint: print(f"Processing event Run {target_run}, Event {target_event}")
        hit_data = defaultdict(list)
        with h5py.File(filename, 'r') as f:
            if self.DebugPrint: print("Reading hit data...")
            hits = np.array(f['SRTTWOfflinePulsesDC'])
            if self.DebugPrint: print("Filtering event hits...")
            event_hits = hits[(hits['Run'] == target_run) & 
                            (hits['Event'] == target_event)]
            
            if self.DebugPrint: print(f"Processing {len(event_hits)} hits...")
            for hit in event_hits:
                string = int(hit['string'])
                om = int(hit['om'])
                hit_data[(string, om)].append((float(hit['time']), float(hit['charge'])))
        return hit_data

    def calculate_time_window(self, hit_data):
        if self.DebugPrint: print("Calculating time window...")
        all_times = []
        for hits in hit_data.values():
            for time, _ in hits:
                all_times.append(time)
                
        if not all_times:
            if self.DebugPrint: print("No hits found in time window")
            return 0, 1
            
        if self.DebugPrint: print("Computing window statistics...")
        median_time = np.median(all_times)
        sorted_times = np.sort(all_times)
        n_hits = len(sorted_times)
        window_size = int(0.9 * n_hits)
        min_range = float('inf')
        time_min = sorted_times[0]
        time_max = sorted_times[-1]
        
        if n_hits > window_size:
            if self.DebugPrint: print("Finding optimal time window...")
            for i in range(n_hits - window_size):
                current_range = sorted_times[i + window_size] - sorted_times[i]
                if current_range < min_range:
                    min_range = current_range
                    time_min = sorted_times[i]
                    time_max = sorted_times[i + window_size]
        return time_min, time_max

    def get_color_for_time(self, time, time_min, time_max):
        if time < time_min:
            return RED
        if time > time_max:
            return PURPLE
        
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        t = (time - time_min) / (time_max - time_min)
        color_idx = t * (len(colors) - 1)
        idx1 = int(color_idx)
        idx2 = min(idx1 + 1, len(colors) - 1)
        t_interp = color_idx - idx1
        return interpolate_color(colors[idx1], colors[idx2], t_interp)

    def create_event_visualization(self, hit_data, run, event):
        if self.DebugPrint: print("Creating visualization...")
        time_min, time_max = self.calculate_time_window(hit_data)
        detector = VGroup()
        
        # Removed because it takes too long.
        #if self.DebugPrint: print("Adding background dots...")
        #for pos in self.module_positions.values():
        #    dot = Sphere(radius=0.02).set_color(WHITE)
        #    dot.move_to(pos)
        #    detector.add(dot)
        
        if hit_data:
            if self.DebugPrint: print("Processing hit modules...")
            max_charge = max(sum(charge for _, charge in hits) 
                           for hits in hit_data.values())
            
            for (string, om), hits in hit_data.items():
                if (string, om) not in self.module_positions:
                    continue
                    
                total_charge = sum(charge for _, charge in hits)
                avg_time = np.mean([time for time, _ in hits])
                
                radius = 0.05 + (total_charge / max_charge) * 0.15
                color = self.get_color_for_time(avg_time, time_min, time_max)
                
                sphere = Sphere(radius=radius)
                sphere.set_color(color)
                sphere.set_opacity(0.8)
                sphere.move_to(self.module_positions[(string, om)])
                detector.add(sphere)
        
        if self.DebugPrint: print("Adding text labels...")
        text = Text(f"Run: {run}\nEvent: {event}")
        text.to_corner(UL)
        text.set_color(WHITE)
        text.scale(0.5)
        return detector, text

    def construct(self):
        filename = 'oscNext_genie_level7_v02.00_pass2.120000.000000.hdf5'
        self.load_geometry()
        events = self.get_event_list(filename)
        
        if self.DebugPrint: print(f"Starting visualization of {self.NEvents} events...")
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        
        for i, (run, event) in enumerate(events):
            hit_data = self.process_event(filename, run, event)
            detector, text = self.create_event_visualization(hit_data, run, event)
            
            if self.DebugPrint: print(f"Rendering event {i+1}/{len(events)}...")
            if i == 0:
                self.play(Create(detector), Write(text))
            else:
                self.play(
                    FadeOut(self.mobjects[-2]),
                    FadeOut(self.mobjects[-1]),
                    FadeIn(detector),
                    Write(text)
                )
            
            self.wait(2)
            
            for phi in [45, 60, 30]:
                self.move_camera(phi=phi * DEGREES, run_time=2)
                self.wait()

def render_visualization(NEvents=1, DebugPrint=True):
    scene = DetectorVisualization(NEvents, DebugPrint)
    config.media_width = "480"
    config.pixel_height = 480
    config.pixel_width = 480
    config.frame_rate = 15
    
    filename = 'oscNext_genie_level7_v02.00_pass2.120000.000000.hdf5'
    with h5py.File(filename, 'r') as f:
        hits = np.array(f['SRTTWOfflinePulsesDC'])
        first_event = np.unique(hits[['Run', 'Event']])[0]
        run, event = first_event
        config.output_file = f"run{run}_event{event}"
    
    scene.render()

if __name__ == "__main__":
    render_visualization()