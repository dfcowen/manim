from manim import *
import h5py
import numpy as np
from collections import defaultdict

class StaticDetectorVisualization(ThreeDScene):
    def __init__(self):
        super().__init__()
        self.module_positions = {}
        self.event_centroid = np.array([0, 0, 0])
        
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
            print(f"Time {time:.2f} below time window, using RED")
            return RED
        if time > time_max:
            print(f"Time {time:.2f} above time window, using PURPLE")
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
            
            # Calculate centroid of hit modules for coordinate system origin
            hit_positions = [np.array(self.module_positions[(string, om)])
                            for (string, om) in hit_data.keys()
                            if (string, om) in self.module_positions]
            
            if hit_positions:
                self.event_centroid = np.mean(hit_positions, axis=0)
                print(f"Event centroid: ({self.event_centroid[0]:.2f}, {self.event_centroid[1]:.2f}, {self.event_centroid[2]:.2f})")
            
            # Identify strings with hits
            hit_strings = {string for (string, om) in hit_data.keys() 
                          if (string, om) in self.module_positions}
            print(f"Strings with hits: {hit_strings}")
            
            # Find min and max z-coordinates of all modules with hits
            z_coords = [self.module_positions[(string, om)][2] 
                       for (string, om) in hit_data.keys() 
                       if (string, om) in self.module_positions]
            
            if z_coords:
                min_z, max_z = min(z_coords), max(z_coords)
                print(f"Z-coordinate range: {min_z:.2f} to {max_z:.2f}")
                
                # Add string lines
                for string in hit_strings:
                    # Find any module on this string to get the x,y position
                    for om in range(1, 61):  # Typical range of OMs per string
                        if (string, om) in self.module_positions:
                            pos = np.array(self.module_positions[(string, om)])
                            x, y = pos[0], pos[1]
                            
                            # Create line relative to centroid
                            start_point = np.array([x, y, min_z]) - self.event_centroid
                            end_point = np.array([x, y, max_z]) - self.event_centroid
                            
                            line = Line(start_point, end_point, color=WHITE, stroke_width=1)
                            detector.add(line)
                            print(f"Added line for string {string} at x={x:.2f}, y={y:.2f}")
                            break
            
            # Add hit modules as spheres
            for (string, om), hits in hit_data.items():
                if (string, om) not in self.module_positions:
                    print(f"Warning: Module ({string}, {om}) not in geometry!")
                    continue
                
                pos = np.array(self.module_positions[(string, om)])
                x, y, z = pos
                # Adjust position relative to centroid
                adjusted_pos = pos - self.event_centroid
                
                print(f"\nProcessing string {string}, OM {om} at x={x:.2f}, y={y:.2f}, z={z:.2f}:")
                
                total_charge = sum(charge for _, charge in hits)
                avg_time = np.mean([time for time, _ in hits])
                
                radius = 0.5 + (total_charge / max_charge) * 1.5
                radius = 3.*radius # geo distances are in meters, so sphere radius needs to be < ~7m (in DeepCore)
                color = self.get_color_for_time(avg_time, time_min, time_max)
                print(f"  Qtot: {total_charge:.2f}, tave: {avg_time:.2f}, rDOM: {radius:.2f}, color: {color}")
                
                sphere = Sphere(radius=radius, resolution=(32, 32))
                sphere.set_color(color)
                sphere.set_opacity(1.0)
                sphere.set_gloss(0.5)
                sphere.set_shadow(0.2)
                sphere.move_to(adjusted_pos)
                detector.add(sphere)
        
        # Create a coordinate axes indicator
        axes_scale = 5.0  # Size of the axes
        origin = np.array([0, 0, 0])  # Centered at origin (which is now the event centroid)
        
        # Create the axes lines
        x_axis = Arrow(origin, origin + np.array([axes_scale, 0, 0]), color=RED, buff=0)
        y_axis = Arrow(origin, origin + np.array([0, axes_scale, 0]), color=GREEN, buff=0)
        z_axis = Arrow(origin, origin + np.array([0, 0, axes_scale]), color=BLUE, buff=0)
        
        # Create the labels
        x_label = Text("x", color=RED).scale(0.5).move_to(origin + np.array([axes_scale + 0.5, 0, 0]))
        y_label = Text("y", color=GREEN).scale(0.5).move_to(origin + np.array([0, axes_scale + 0.5, 0]))
        z_label = Text("z", color=BLUE).scale(0.5).move_to(origin + np.array([0, 0, axes_scale + 0.5]))
        
        axes = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        
        print("\nAdding text, axes, and finalizing scene...")
        text = Text(f"Run: {run}\nEvent: {event}")
        text.to_corner(UR)
        text.set_color(WHITE)
        text.scale(0.5)
        
        self.add(detector, axes, text)
        
        # Set up a side view with z-axis running vertically
        # phi=90 gives a view perpendicular to the z-axis
        # theta controls the rotation around the z-axis (0, 90, 180, 270 give different side views)
        self.set_camera_orientation(phi=90 * DEGREES, theta=0 * DEGREES, focal_distance=8)
        self.camera.light_source.move_to(10*RIGHT + 10*IN + 10*UP)
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