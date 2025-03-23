from manim import *
import h5py
import numpy as np
from collections import defaultdict

class DetectorVisualization(ThreeDScene):
    def __init__(self):
        super().__init__()
        self.module_positions = {}  # (string, om) -> (x, y, z)
        self.hit_data = defaultdict(list)  # (string, om) -> [(time, charge)]
        
    def load_geometry(self):
        with h5py.File('GeoCalibDetectorStatus_AVG_55697-57531_PASS2_SPE_withScaledNoise.hdf5', 'r') as f:
            geo_data = np.array(f['geo'])
            labels = np.array([label.decode('utf-8') for label in f['labels']])
            
            # Create mapping of column names to indices
            col_indices = {label: idx for idx, label in enumerate(labels)}
            
            # Store module positions
            print(f'Looping over rows in geo_data')
            for row in geo_data:
                string = int(row[col_indices['string']])
                om = int(row[col_indices['om']])
                pos = (
                    float(row[col_indices['pos_x']]),
                    float(row[col_indices['pos_y']]),
                    float(row[col_indices['pos_z']])
                )
                self.module_positions[(string, om)] = pos

    def load_event_data(self, filename, target_run, target_event):
        with h5py.File(filename, 'r') as f:
            hits = np.array(f['SRTTWOfflinePulsesDC'])
            
            # Filter hits for specific run and event
            event_hits = hits[
                (hits['Run'] == target_run) & 
                (hits['Event'] == target_event)
            ]
            
            # Group hits by module
            print(f'Group hits by module')
            for hit in event_hits:
                string = int(hit['string'])
                om = int(hit['om'])
                self.hit_data[(string, om)].append((float(hit['time']), float(hit['charge'])))

    def calculate_time_window(self):
        print(f'Find time window')
        #all_times = [time for hits in self.hit_data.values() for time, _ in hits]
        all_times = []
        for hits in self.hit_data.values():
            print(f'Length of hits: {len(hits)}')
            for time, charge in hits:
                all_times.append(time)
        print(f'Length of all_times: {len(all_times)}')
        median_time = np.median(all_times)
        sorted_times = np.sort(all_times)
        
        # Find window containing 90% of hits
        n_hits = len(sorted_times)
        window_size = int(0.9 * n_hits)
        min_range = float('inf')
        
        for i in range(n_hits - window_size):
            current_range = sorted_times[i + window_size] - sorted_times[i]
            if current_range < min_range:
                min_range = current_range
                self.time_min = sorted_times[i]
                self.time_max = sorted_times[i + window_size]

    def get_color_for_time(self, time):
        if time < self.time_min:
            return RED
        if time > self.time_max:
            return PURPLE
            
        # Rainbow color interpolation
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        t = (time - self.time_min) / (self.time_max - self.time_min)
        color_idx = t * (len(colors) - 1)
        idx1 = int(color_idx)
        idx2 = min(idx1 + 1, len(colors) - 1)
        t_interp = color_idx - idx1
        return interpolate_color(colors[idx1], colors[idx2], t_interp)

    def construct(self):
        # Load data
        print(f'Loading geo_data and assigning labels and col_indices')
        self.load_geometry()
        target_run = 120000  # Example run/event numbers
        target_event = 1

        print(f'Loading hits from oscNext_genie_level7_v02.00_pass2.120000.000000.hdf5')
        print(f'Selecting hits from run {target_run} and event {target_event}')
        self.load_event_data('oscNext_genie_level7_v02.00_pass2.120000.000000.hdf5', target_run, target_event)
        self.calculate_time_window()

        # Create visualization
        detector = VGroup()
        
        # Add white dots for all modules
        for pos in self.module_positions.values():
            dot = Sphere(radius=0.02).set_color(WHITE)
            dot.move_to(pos)
            detector.add(dot)
            
        # Add colored spheres for hit modules
        print(f'Assign colors to light arrival times')
        max_charge = max(sum(charge for _, charge in hits) 
                        for hits in self.hit_data.values())
        
        for (string, om), hits in self.hit_data.items():
            if (string, om) not in self.module_positions:
                continue
                
            total_charge = sum(charge for _, charge in hits)
            avg_time = np.mean([time for time, _ in hits])
            
            radius = 0.05 + (total_charge / max_charge) * 0.15
            color = self.get_color_for_time(avg_time)
            
            sphere = Sphere(radius=radius)
            sphere.set_color(color)
            sphere.set_opacity(0.8)
            sphere.move_to(self.module_positions[(string, om)])
            detector.add(sphere)

        # Add run/event text
        text = Text(f"Run: {target_run}\nEvent: {target_event}")
        text.to_corner(UL)
        text.set_color(WHITE)
        text.scale(0.5)
        
        # Set up camera and animation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        
        self.play(Create(detector), Write(text))
        self.wait(2)
        
        # Multiple viewing angles
        for phi in [45, 60, 30]:
            self.move_camera(phi=phi * DEGREES, run_time=2)
            self.wait()

def render_visualization():
    scene = DetectorVisualization()
    scene.render()

if __name__ == "__main__":
    render_visualization()