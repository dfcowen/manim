from manim import *
import h5py
import numpy as np
from collections import defaultdict

class StaticDetectorVisualization(ThreeDScene):
    def __init__(self):
        super().__init__()
        self.module_positions = {}
        
    def load_geometry(self):
        print("Loading geometry file...")
        with h5py.File('GeoCalibDetectorStatus_AVG_55697-57531_PASS2_SPE_withScaledNoise.hdf5', 'r') as f:
            print("Reading geometry data...")
            geo_data = np.array(f['geo'])
            labels = np.array([label.decode('utf-8') for label in f['labels']])
            col_indices = {label: idx for idx, label in enumerate(labels)}
            
            print("Processing geometry rows...")
            for row in geo_data:
                string = int(row[col_indices['string']])
                om = int(row[col_indices['om']])
                pos = (float(row[col_indices['pos_x']]),
                      float(row[col_indices['pos_y']]),
                      float(row[col_indices['pos_z']]))
                self.module_positions[(string, om)] = pos
            print(f"Loaded {len(self.module_positions)} module positions")

    def process_event(self, filename, target_run, target_event):
        print(f"Processing event {target_run}, {target_event}")
        hit_data = defaultdict(list)
        with h5py.File(filename, 'r') as f:
            print("Reading hit data...")
            hits = np.array(f['SRTTWOfflinePulsesDC'])
            event_hits = hits[(hits['Run'] == target_run) & 
                            (hits['Event'] == target_event)]
            
            print(f"Found {len(event_hits)} hits for this event")
            for hit in event_hits:
                string = int(hit['string'])
                om = int(hit['om'])
                hit_data[(string, om)].append((float(hit['time']), float(hit['charge'])))
            print(f"Grouped hits into {len(hit_data)} modules")
        return hit_data

    def calculate_time_window(self, hit_data):
        print("Calculating time window...")
        all_times = []
        for hits in hit_data.values():
            for time, _ in hits:
                all_times.append(time)
                
        if not all_times:
            print("No hits found!")
            return 0, 1
            
        sorted_times = np.sort(all_times)
        n_hits = len(sorted_times)
        window_size = int(0.9 * n_hits)
        min_range = float('inf')
        time_min = sorted_times[0]
        time_max = sorted_times[-1]

        print(f'Initial time range: {time_min:.2f} to {time_max:.2f}')
        
        if n_hits > window_size:
            print(f"Finding optimal window for {n_hits} hits...")
            for i in range(n_hits - window_size):
                current_range = sorted_times[i + window_size] - sorted_times[i]
                if current_range < min_range:
                    min_range = current_range
                    time_min = sorted_times[i]
                    time_max = sorted_times[i + window_size]
        print(f'Final time window: {time_min:.2f} to {time_max:.2f}')
        return time_min, time_max

    def get_color_for_time(self, time, time_min, time_max):
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        if time < time_min:
            print(f"Time {time:.2f} below window, using RED")
            return RED
        if time > time_max:
            print(f"Time {time:.2f} above window, using PURPLE")
            return PURPLE
        
        t = (time - time_min) / (time_max - time_min)
        color_idx = t * (len(colors) - 1)
        idx1 = int(color_idx)
        idx2 = min(idx1 + 1, len(colors) - 1)
        t_interp = color_idx - idx1
        return interpolate_color(colors[idx1], colors[idx2], t_interp)

    def create_visualization(self, run, event):
        print(f"\nCreating visualization for Run {run}, Event {event}")
        filename = 'oscNext_genie_level7_v02.00_pass2.120000.000000.hdf5'
        self.load_geometry()
        hit_data = self.process_event(filename, run, event)
        
        time_min, time_max = self.calculate_time_window(hit_data)
        detector = VGroup()
        
        if hit_data:
            print("\nProcessing hits for visualization...")
            max_charge = max(sum(charge for _, charge in hits) 
                           for hits in hit_data.values())
            print(f"Maximum total charge in any module: {max_charge:.2f}")
            
            for (string, om), hits in hit_data.items():
                print(f"\nProcessing string {string}, OM {om}:")
                if (string, om) not in self.module_positions:
                    print(f"Warning: Module ({string}, {om}) not in geometry!")
                    continue
                    
                total_charge = sum(charge for _, charge in hits)
                avg_time = np.mean([time for time, _ in hits])
                print(f"  Total charge: {total_charge:.2f}")
                print(f"  Average time: {avg_time:.2f}")
                
                radius = 0.5 + (total_charge / max_charge) * 1.5
                radius = 3.*radius # geo distances are in meters, so sphere radius needs to be < ~7m (in DeepCore)
                color = self.get_color_for_time(avg_time, time_min, time_max)
                print(f"  Sphere radius: {radius:.2f}")
                print(f"  Sphere color: {color}")
                
                sphere = Sphere(radius=radius, resolution=(32, 32))
                sphere.set_color(color)
                sphere.set_opacity(1.0)
                sphere.set_gloss(0.5)
                sphere.set_shadow(0.2)
                sphere.move_to(self.module_positions[(string, om)])
                print(f'Moving (string,om) = ({string},{om}) to {self.module_positions[(string, om)]}')
                detector.add(sphere)
        
        print("\nAdding text and finalizing scene...")
        text = Text(f"Run: {run}\nEvent: {event}")
        text.to_corner(UL)
        text.set_color(WHITE)
        text.scale(0.5)
        
        self.add(detector, text)
        #self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, focal_distance=1)
        self.set_camera_orientation(phi=0 * DEGREES, theta=0 * DEGREES, focal_distance=16)
        self.camera.light_source.move_to(3*IN + 3*RIGHT + UP)
        self.wait(0)

def render_static_image(run, event):
    print(f"\nStarting render for Run {run}, Event {event}")
    config.media_width = "480"
    config.pixel_height = 480
    config.pixel_width = 480
    config.save_last_frame = True
    config.write_to_movie = False
    
    scene = StaticDetectorVisualization()
    config.output_file = f"run{run}_event{event}"
    print("Configuration complete, creating visualization...")
    scene.create_visualization(run, event)
    print("Rendering final image...")
    scene.render()

if __name__ == "__main__":
    print("Starting event visualization script...")
    filename = 'oscNext_genie_level7_v02.00_pass2.120000.000000.hdf5' # nue(?)
    #filename = 'oscNext_genie_level7_v02.00_pass2.140000.000001.hdf5' # numu 
    print(f"Reading events from {filename}")
#    with h5py.File(filename, 'r') as f:
#        hits = np.array(f['SRTTWOfflinePulsesDC'])
#        first_event = np.unique(hits[['Run', 'Event']])[0]
#        run, event = first_event
#        print(f"Selected Run {run}, Event {event}")

    NMinModules = 25
    with h5py.File(filename, 'r') as f:
        hits = np.array(f['SRTTWOfflinePulsesDC'])
        events = np.unique(hits[['Run', 'Event']])
        
        for event_idx, (run, event) in enumerate(events):
            event_hits = hits[(hits['Run'] == run) & (hits['Event'] == event)]
            n_modules = len(np.unique(event_hits[['string', 'om']], axis=0))
            
            if n_modules >= NMinModules:
                print(f"Found event {run}, {event} with {n_modules} hit modules")
                break
                
            if event_idx == len(events)-1:
                print(f"No events found with >= {NMinModules} hit modules")
                run, event = events[0] # Use first event as fallback

    render_static_image(run, event)