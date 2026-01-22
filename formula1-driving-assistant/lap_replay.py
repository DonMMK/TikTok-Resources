"""
Formula 1 Driving Assistant - Lap Replay Animation Module

Animated lap replay with:
- Car moving through the track in real-time
- Live telemetry display (speed, throttle, brake, gear)
- Play/Pause/Stop controls
- Steering wheel visualization
- Progress bar showing lap position
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
import matplotlib.gridspec as gridspec
import numpy as np
from typing import Optional, Tuple, Callable

from data_loader import TelemetryData, DrivingZones


# Color scheme
COLORS = {
    'background': '#1a1a2e',
    'track': '#444444',
    'track_edge': '#666666',
    'car': '#FF0000',
    'car_trail': '#FF6600',
    'throttle': '#00FF00',
    'brake': '#FF0000',
    'text': '#FFFFFF',
    'text_dim': '#888888',
    'gauge_bg': '#333333',
    'speed_bar': '#00AAFF',
    'gear_bg': '#222222',
}


class LapReplayAnimation:
    """
    Animated lap replay with telemetry visualization.
    
    Controls:
    - Space: Play/Pause
    - R: Reset to start
    - Left/Right arrows: Step frame by frame
    - +/-: Speed up/slow down
    """
    
    def __init__(
        self,
        telemetry: TelemetryData,
        zones: Optional[DrivingZones] = None,
        title: str = "Lap Replay",
        rotation: float = 0.0,
        fps: int = 30,
        playback_speed: float = 1.0
    ):
        self.telemetry = telemetry
        self.zones = zones
        self.title = title
        self.rotation = rotation
        self.fps = fps
        self.playback_speed = playback_speed
        
        # Animation state
        self.current_frame = 0
        self.is_playing = False
        self.total_frames = len(telemetry.speed)
        
        # Calculate frame skip based on time data for real-time playback
        self.time_data = telemetry.time
        self.lap_duration = self.time_data[-1] - self.time_data[0]
        
        # Prepare rotated coordinates
        self.x, self.y = self._rotate_coords(telemetry.x, telemetry.y)
        
        # Setup the figure
        self._setup_figure()
        self._setup_controls()
        
        # Animation object
        self.animation = None
    
    def _rotate_coords(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Rotate coordinates by the circuit rotation angle."""
        if self.rotation == 0:
            return x.copy(), y.copy()
        
        angle_rad = np.radians(self.rotation)
        cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
        
        cx, cy = x.mean(), y.mean()
        x_centered = x - cx
        y_centered = y - cy
        
        x_rot = x_centered * cos_a - y_centered * sin_a + cx
        y_rot = x_centered * sin_a + y_centered * cos_a + cy
        
        return x_rot, y_rot
    
    def _setup_figure(self):
        """Setup the matplotlib figure with track and telemetry panels."""
        self.fig = plt.figure(figsize=(16, 10), facecolor=COLORS['background'])
        self.fig.canvas.manager.set_window_title(self.title)
        
        # Create grid: main track area + side panel for telemetry
        gs = gridspec.GridSpec(3, 4, figure=self.fig, 
                               height_ratios=[1, 0.3, 0.15],
                               width_ratios=[3, 1, 1, 1],
                               hspace=0.3, wspace=0.3)
        
        # Main track view (spans left 3 columns, top row)
        self.ax_track = self.fig.add_subplot(gs[0, :3])
        self.ax_track.set_facecolor(COLORS['background'])
        self.ax_track.set_aspect('equal')
        self.ax_track.axis('off')
        
        # Telemetry panel (right column, top row)
        self.ax_telemetry = self.fig.add_subplot(gs[0, 3])
        self.ax_telemetry.set_facecolor(COLORS['background'])
        self.ax_telemetry.axis('off')
        
        # Throttle/Brake bars (middle row)
        self.ax_inputs = self.fig.add_subplot(gs[1, :3])
        self.ax_inputs.set_facecolor(COLORS['background'])
        
        # Progress/time display (bottom row, will add controls here)
        self.ax_progress = self.fig.add_subplot(gs[2, :3])
        self.ax_progress.set_facecolor(COLORS['background'])
        
        # Draw static elements
        self._draw_track()
        self._setup_telemetry_display()
        self._setup_input_bars()
        self._setup_progress_bar()
        
        # Create dynamic elements (car marker, etc.)
        self._create_dynamic_elements()
    
    def _draw_track(self):
        """Draw the static track layout."""
        # Track outline
        self.ax_track.plot(self.x, self.y, color=COLORS['track_edge'], 
                          linewidth=15, alpha=0.4, zorder=1)
        self.ax_track.plot(self.x, self.y, color=COLORS['track'], 
                          linewidth=10, alpha=0.8, zorder=2)
        
        # Start/finish marker
        self.ax_track.scatter(self.x[0], self.y[0], s=200, c='white', 
                             marker='s', zorder=5, edgecolors='green', linewidths=3)
        
        # Title
        self.ax_track.set_title(self.title, color=COLORS['text'], 
                               fontsize=14, fontweight='bold', pad=10)
        
        # Set limits with padding
        padding = (self.x.max() - self.x.min()) * 0.1
        self.ax_track.set_xlim(self.x.min() - padding, self.x.max() + padding)
        self.ax_track.set_ylim(self.y.min() - padding, self.y.max() + padding)
    
    def _setup_telemetry_display(self):
        """Setup the telemetry information panel."""
        self.ax_telemetry.set_xlim(0, 1)
        self.ax_telemetry.set_ylim(0, 1)
        
        # Static labels
        labels = [
            (0.5, 0.95, "TELEMETRY", 14, 'bold'),
            (0.1, 0.82, "SPEED", 10, 'normal'),
            (0.1, 0.62, "GEAR", 10, 'normal'),
            (0.1, 0.42, "THROTTLE", 10, 'normal'),
            (0.1, 0.22, "BRAKE", 10, 'normal'),
            (0.1, 0.05, "LAP TIME", 10, 'normal'),
        ]
        
        for x, y, text, size, weight in labels:
            self.ax_telemetry.text(x, y, text, color=COLORS['text_dim'],
                                  fontsize=size, fontweight=weight,
                                  ha='center' if y == 0.95 else 'left')
        
        # Dynamic value text objects (will be updated)
        self.speed_text = self.ax_telemetry.text(0.9, 0.82, "0", color=COLORS['text'],
                                                  fontsize=20, fontweight='bold', ha='right')
        self.speed_unit = self.ax_telemetry.text(0.92, 0.80, "km/h", color=COLORS['text_dim'],
                                                  fontsize=8, ha='left')
        
        self.gear_text = self.ax_telemetry.text(0.5, 0.55, "N", color=COLORS['text'],
                                                fontsize=36, fontweight='bold', ha='center',
                                                bbox=dict(boxstyle='round,pad=0.3', 
                                                         facecolor=COLORS['gear_bg'], 
                                                         edgecolor=COLORS['text_dim']))
        
        self.throttle_text = self.ax_telemetry.text(0.9, 0.42, "0%", color=COLORS['throttle'],
                                                    fontsize=16, fontweight='bold', ha='right')
        
        self.brake_text = self.ax_telemetry.text(0.9, 0.22, "0%", color=COLORS['brake'],
                                                 fontsize=16, fontweight='bold', ha='right')
        
        self.time_text = self.ax_telemetry.text(0.9, 0.05, "0:00.000", color=COLORS['text'],
                                                fontsize=14, fontweight='bold', ha='right')
    
    def _setup_input_bars(self):
        """Setup throttle and brake visualization bars."""
        self.ax_inputs.set_xlim(0, 100)
        self.ax_inputs.set_ylim(0, 2)
        self.ax_inputs.axis('off')
        
        # Background bars
        self.ax_inputs.barh([1.2], [100], height=0.5, color=COLORS['gauge_bg'], alpha=0.5)
        self.ax_inputs.barh([0.3], [100], height=0.5, color=COLORS['gauge_bg'], alpha=0.5)
        
        # Labels
        self.ax_inputs.text(-2, 1.2, "THR", color=COLORS['throttle'], fontsize=10, 
                           fontweight='bold', ha='right', va='center')
        self.ax_inputs.text(-2, 0.3, "BRK", color=COLORS['brake'], fontsize=10,
                           fontweight='bold', ha='right', va='center')
        
        # Dynamic bars (will be updated)
        self.throttle_bar = self.ax_inputs.barh([1.2], [0], height=0.5, 
                                                 color=COLORS['throttle'], alpha=0.8)[0]
        self.brake_bar = self.ax_inputs.barh([0.3], [0], height=0.5,
                                              color=COLORS['brake'], alpha=0.8)[0]
    
    def _setup_progress_bar(self):
        """Setup the lap progress bar."""
        self.ax_progress.set_xlim(0, 100)
        self.ax_progress.set_ylim(0, 1)
        self.ax_progress.axis('off')
        
        # Background
        self.ax_progress.barh([0.5], [100], height=0.3, color=COLORS['gauge_bg'], alpha=0.5)
        
        # Progress bar (dynamic)
        self.progress_bar = self.ax_progress.barh([0.5], [0], height=0.3,
                                                   color=COLORS['speed_bar'], alpha=0.8)[0]
        
        # Distance markers
        for pct in [0, 25, 50, 75, 100]:
            self.ax_progress.axvline(x=pct, color=COLORS['text_dim'], linewidth=0.5, alpha=0.3)
            self.ax_progress.text(pct, 0.1, f"{pct}%", color=COLORS['text_dim'],
                                 fontsize=8, ha='center')
    
    def _create_dynamic_elements(self):
        """Create elements that will be updated during animation."""
        # Car marker on track
        self.car_marker, = self.ax_track.plot([], [], 'o', color=COLORS['car'],
                                               markersize=15, zorder=10,
                                               markeredgecolor='white', markeredgewidth=2)
        
        # Trail behind car (last N positions)
        self.trail_length = 50
        self.trail_line, = self.ax_track.plot([], [], '-', color=COLORS['car_trail'],
                                               linewidth=3, alpha=0.6, zorder=9)
    
    def _setup_controls(self):
        """Setup play/pause/reset buttons."""
        # Button axes
        ax_play = self.fig.add_axes([0.35, 0.02, 0.08, 0.04])
        ax_pause = self.fig.add_axes([0.44, 0.02, 0.08, 0.04])
        ax_reset = self.fig.add_axes([0.53, 0.02, 0.08, 0.04])
        ax_speed = self.fig.add_axes([0.65, 0.02, 0.15, 0.04])
        
        # Buttons
        self.btn_play = Button(ax_play, '▶ Play', color=COLORS['gauge_bg'], 
                               hovercolor=COLORS['throttle'])
        self.btn_pause = Button(ax_pause, '⏸ Pause', color=COLORS['gauge_bg'],
                                hovercolor=COLORS['text_dim'])
        self.btn_reset = Button(ax_reset, '⏹ Reset', color=COLORS['gauge_bg'],
                                hovercolor=COLORS['brake'])
        
        # Speed slider
        self.slider_speed = Slider(ax_speed, 'Speed', 0.25, 4.0, 
                                   valinit=self.playback_speed, valstep=0.25,
                                   color=COLORS['speed_bar'])
        
        # Connect callbacks
        self.btn_play.on_clicked(self._on_play)
        self.btn_pause.on_clicked(self._on_pause)
        self.btn_reset.on_clicked(self._on_reset)
        self.slider_speed.on_changed(self._on_speed_change)
        
        # Keyboard controls
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        
        # Instructions
        self.fig.text(0.02, 0.02, "Controls: Space=Play/Pause | R=Reset | ←→=Step | +/-=Speed",
                     color=COLORS['text_dim'], fontsize=9)
    
    def _on_play(self, event=None):
        """Start playback."""
        if not self.is_playing:
            self.is_playing = True
            if self.animation is None:
                self._start_animation()
    
    def _on_pause(self, event=None):
        """Pause playback."""
        self.is_playing = False
    
    def _on_reset(self, event=None):
        """Reset to beginning."""
        self.is_playing = False
        self.current_frame = 0
        self._update_frame(0)
    
    def _on_speed_change(self, val):
        """Update playback speed."""
        self.playback_speed = val
    
    def _on_key_press(self, event):
        """Handle keyboard input."""
        if event.key == ' ':
            if self.is_playing:
                self._on_pause()
            else:
                self._on_play()
        elif event.key == 'r':
            self._on_reset()
        elif event.key == 'right':
            self.current_frame = min(self.current_frame + 10, self.total_frames - 1)
            self._update_frame(self.current_frame)
        elif event.key == 'left':
            self.current_frame = max(self.current_frame - 10, 0)
            self._update_frame(self.current_frame)
        elif event.key == '+' or event.key == '=':
            self.playback_speed = min(self.playback_speed + 0.25, 4.0)
            self.slider_speed.set_val(self.playback_speed)
        elif event.key == '-':
            self.playback_speed = max(self.playback_speed - 0.25, 0.25)
            self.slider_speed.set_val(self.playback_speed)
    
    def _update_frame(self, frame_idx: int) -> list:
        """Update all dynamic elements for a given frame."""
        frame_idx = int(frame_idx) % self.total_frames
        
        # Update car position
        car_x, car_y = self.x[frame_idx], self.y[frame_idx]
        self.car_marker.set_data([car_x], [car_y])
        
        # Update trail
        trail_start = max(0, frame_idx - self.trail_length)
        self.trail_line.set_data(self.x[trail_start:frame_idx+1], 
                                  self.y[trail_start:frame_idx+1])
        
        # Update telemetry values
        speed = self.telemetry.speed[frame_idx]
        gear = int(self.telemetry.gear[frame_idx])
        throttle = self.telemetry.throttle[frame_idx]
        brake = self.telemetry.brake[frame_idx]
        
        # Normalize brake (might be 0-1 or 0-100)
        if brake <= 1:
            brake = brake * 100
        
        self.speed_text.set_text(f"{speed:.0f}")
        self.gear_text.set_text(str(gear) if gear > 0 else "N")
        self.throttle_text.set_text(f"{throttle:.0f}%")
        self.brake_text.set_text(f"{brake:.0f}%")
        
        # Update input bars
        self.throttle_bar.set_width(throttle)
        self.brake_bar.set_width(brake)
        
        # Update time
        current_time = self.telemetry.time[frame_idx] - self.telemetry.time[0]
        minutes = int(current_time // 60)
        seconds = current_time % 60
        self.time_text.set_text(f"{minutes}:{seconds:06.3f}")
        
        # Update progress bar
        progress = (frame_idx / self.total_frames) * 100
        self.progress_bar.set_width(progress)
        
        return [self.car_marker, self.trail_line, self.throttle_bar, self.brake_bar,
                self.speed_text, self.gear_text, self.throttle_text, self.brake_text,
                self.time_text, self.progress_bar]
    
    def _animate(self, frame):
        """Animation function called each frame."""
        if self.is_playing:
            # Calculate frame step based on playback speed
            # We want real-time playback at speed=1.0
            frames_per_interval = int(self.playback_speed * (self.total_frames / (self.lap_duration * self.fps)))
            frames_per_interval = max(1, frames_per_interval)
            
            self.current_frame += frames_per_interval
            if self.current_frame >= self.total_frames:
                self.current_frame = 0  # Loop
        
        return self._update_frame(self.current_frame)
    
    def _start_animation(self):
        """Initialize and start the animation."""
        interval = 1000 / self.fps  # milliseconds between frames
        self.animation = FuncAnimation(
            self.fig,
            self._animate,
            interval=interval,
            blit=False,  # blit=True can cause issues with text updates
            cache_frame_data=False
        )
    
    def show(self):
        """Display the replay window."""
        self._start_animation()
        plt.show()
    
    def close(self):
        """Close the replay window."""
        if self.animation:
            self.animation.event_source.stop()
        plt.close(self.fig)


def run_lap_replay(
    telemetry: TelemetryData,
    zones: Optional[DrivingZones] = None,
    title: str = "Lap Replay",
    rotation: float = 0.0
):
    """
    Convenience function to create and run a lap replay.
    
    Args:
        telemetry: TelemetryData object with lap telemetry
        zones: Optional DrivingZones for additional context
        title: Window title
        rotation: Circuit rotation in degrees
    """
    replay = LapReplayAnimation(
        telemetry=telemetry,
        zones=zones,
        title=title,
        rotation=rotation
    )
    replay.show()


if __name__ == "__main__":
    # Test the replay
    from data_loader import load_session, get_lap_telemetry, analyze_driving_zones, get_fastest_lap_info, get_circuit_info
    
    print("Loading test data...")
    session = load_session(2024, 1, 'Q')  # Bahrain 2024 Qualifying
    
    lap_info = get_fastest_lap_info(session)
    print(f"Fastest lap: {lap_info.driver} - {lap_info.lap_time}" if lap_info else "No lap info")
    
    telemetry = get_lap_telemetry(session)
    if telemetry:
        zones = analyze_driving_zones(telemetry)
        circuit_info = get_circuit_info(session)
        
        title = f"Bahrain GP 2024 - {lap_info.driver if lap_info else 'Fastest'} ({lap_info.lap_time if lap_info else ''})"
        
        print("Starting replay...")
        run_lap_replay(
            telemetry=telemetry,
            zones=zones,
            title=title,
            rotation=circuit_info.get('rotation', 0)
        )
    else:
        print("Failed to load telemetry")
