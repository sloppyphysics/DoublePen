"""
Double Pendulum Visualization and Animation

This module provides functions to visualize and animate the double pendulum system.
Includes static plots, trajectory traces, phase space diagrams, and MP4 animation export.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from double_pendulum import DoublePendulum


def plot_trajectory_analysis(pendulum, t, trajectory, save_path=None):
    """
    Create a comprehensive visualization of the double pendulum motion.
    
    Parameters
    ----------
    pendulum : DoublePendulum
        The pendulum system object
    t : ndarray
        Time array
    trajectory : ndarray
        Trajectory array of shape (n_points, 4)
    save_path : str, optional
        Path to save the figure. If None, displays the plot.
    """
    fig = plt.figure(figsize=(15, 12))
    
    # Extract states
    theta1 = trajectory[:, 0]
    theta1_dot = trajectory[:, 1]
    theta2 = trajectory[:, 2]
    theta2_dot = trajectory[:, 3]
    
    # Get Cartesian coordinates
    x1, y1, x2, y2 = pendulum.get_cartesian_coords(trajectory)
    
    # Calculate energy
    energy = np.array([pendulum.get_energy(state) for state in trajectory])
    energy_normalized = (energy - energy[0]) / abs(energy[0]) * 100
    
    # 1. Trajectory in 2D space
    ax1 = plt.subplot(3, 3, 1)
    ax1.plot(x2, y2, 'b-', linewidth=0.5, alpha=0.7)
    ax1.plot(x2[0], y2[0], 'go', markersize=10, label='Start')
    ax1.plot(x2[-1], y2[-1], 'r*', markersize=15, label='End')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_title('Trajectory of Mass 2')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.axis('equal')
    
    # 2. Theta1 vs time
    ax2 = plt.subplot(3, 3, 2)
    ax2.plot(t, np.degrees(theta1), 'b-', linewidth=1)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('θ₁ (degrees)')
    ax2.set_title('First Angle vs Time')
    ax2.grid(True, alpha=0.3)
    
    # 3. Theta2 vs time
    ax3 = plt.subplot(3, 3, 3)
    ax3.plot(t, np.degrees(theta2), 'r-', linewidth=1)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('θ₂ (degrees)')
    ax3.set_title('Second Angle vs Time')
    ax3.grid(True, alpha=0.3)
    
    # 4. Theta1 dot vs time
    ax4 = plt.subplot(3, 3, 4)
    ax4.plot(t, theta1_dot, 'b-', linewidth=1)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('θ̇₁ (rad/s)')
    ax4.set_title('First Angular Velocity vs Time')
    ax4.grid(True, alpha=0.3)
    
    # 5. Theta2 dot vs time
    ax5 = plt.subplot(3, 3, 5)
    ax5.plot(t, theta2_dot, 'r-', linewidth=1)
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('θ̇₂ (rad/s)')
    ax5.set_title('Second Angular Velocity vs Time')
    ax5.grid(True, alpha=0.3)
    
    # 6. Energy conservation
    ax6 = plt.subplot(3, 3, 6)
    ax6.plot(t, energy_normalized, 'g-', linewidth=1)
    ax6.set_xlabel('Time (s)')
    ax6.set_ylabel('Energy Deviation (%)')
    ax6.set_title('Energy Conservation Check')
    ax6.grid(True, alpha=0.3)
    ax6.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    
    # 7. Phase space: theta1 vs theta1_dot
    ax7 = plt.subplot(3, 3, 7)
    scatter = ax7.scatter(theta1, theta1_dot, c=t, cmap='viridis', s=1, alpha=0.5)
    ax7.set_xlabel('θ₁ (rad)')
    ax7.set_ylabel('θ̇₁ (rad/s)')
    ax7.set_title('Phase Space: First Pendulum')
    ax7.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax7, label='Time (s)')
    
    # 8. Phase space: theta2 vs theta2_dot
    ax8 = plt.subplot(3, 3, 8)
    scatter = ax8.scatter(theta2, theta2_dot, c=t, cmap='plasma', s=1, alpha=0.5)
    ax8.set_xlabel('θ₂ (rad)')
    ax8.set_ylabel('θ̇₂ (rad/s)')
    ax8.set_title('Phase Space: Second Pendulum')
    ax8.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax8, label='Time (s)')
    
    # 9. Distance between masses
    ax9 = plt.subplot(3, 3, 9)
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    ax9.plot(t, distance, 'm-', linewidth=1)
    ax9.axhline(y=pendulum.L2, color='k', linestyle='--', linewidth=1, label='L₂')
    ax9.set_xlabel('Time (s)')
    ax9.set_ylabel('Distance (m)')
    ax9.set_title('Distance Between Masses')
    ax9.grid(True, alpha=0.3)
    ax9.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {save_path}")
    else:
        plt.show()


def animate_pendulum(pendulum, t, trajectory, interval=50, save_path=None):
    """
    Create an animation of the double pendulum motion.
    
    Parameters
    ----------
    pendulum : DoublePendulum
        The pendulum system object
    t : ndarray
        Time array
    trajectory : ndarray
        Trajectory array of shape (n_points, 4)
    interval : int
        Delay between frames in milliseconds
    save_path : str, optional
        Path to save the animation as MP4. If None, displays animation.
    """
    # Get Cartesian coordinates
    x1, y1, x2, y2 = pendulum.get_cartesian_coords(trajectory)
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Double Pendulum Animation')
    
    # Plot elements
    line, = ax.plot([], [], 'o-', lw=2, markersize=8, color='blue', label='Pendulum')
    trace, = ax.plot([], [], '-', lw=0.5, color='red', alpha=0.3, label='Trace')
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
    ax.legend(loc='upper right')
    
    # Store trace points
    trace_x = []
    trace_y = []
    max_trace_points = 300
    
    def init():
        line.set_data([], [])
        trace.set_data([], [])
        time_text.set_text('')
        return line, trace, time_text
    
    def animate_func(frame):
        # Current positions
        pivot_x, pivot_y = 0, 0
        
        # Update pendulum line
        line.set_data(
            [pivot_x, x1[frame], x2[frame]],
            [pivot_y, y1[frame], y2[frame]]
        )
        
        # Update trace
        trace_x.append(x2[frame])
        trace_y.append(y2[frame])
        if len(trace_x) > max_trace_points:
            trace_x.pop(0)
            trace_y.pop(0)
        trace.set_data(trace_x, trace_y)
        
        # Update time display
        time_text.set_text(f'Time: {t[frame]:.2f}s')
        
        return line, trace, time_text
    
    anim = animation.FuncAnimation(
        fig, animate_func, init_func=init,
        frames=len(t), interval=interval,
        blit=True, repeat=True
    )
    
    if save_path:
        print(f"Saving animation to {save_path}...")
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=30, bitrate=1800)
        anim.save(save_path, writer=writer)
        print(f"Animation saved to {save_path}")
    else:
        plt.show()


def compare_trajectories(pendulum, t_span, num_points=1000, epsilon=0.01):
    """
    Demonstrate sensitivity to initial conditions (chaos).
    
    Parameters
    ----------
    pendulum : DoublePendulum
        The pendulum system object
    t_span : tuple
        (t_start, t_end) time range
    num_points : int
        Number of time points
    epsilon : float
        Small perturbation in initial conditions
    """
    # Two nearly identical initial states
    state1 = np.array([np.pi/2, 0.0, np.pi/2, 0.0])
    state2 = state1 + np.array([epsilon, 0, 0, 0])
    
    # Simulate both
    t, traj1 = pendulum.simulate(state1, t_span, num_points)
    _, traj2 = pendulum.simulate(state2, t_span, num_points)
    
    # Get coordinates
    x1_a, y1_a, x2_a, y2_a = pendulum.get_cartesian_coords(traj1)
    x1_b, y1_b, x2_b, y2_b = pendulum.get_cartesian_coords(traj2)
    
    # Calculate divergence
    divergence = np.sqrt((x2_a - x2_b)**2 + (y2_a - y2_b)**2)
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Trajectories
    axes[0].plot(x2_a, y2_a, 'b-', linewidth=1, label='Initial trajectory', alpha=0.7)
    axes[0].plot(x2_b, y2_b, 'r-', linewidth=1, label=f'Perturbed (ε={epsilon})', alpha=0.7)
    axes[0].set_xlabel('X (m)')
    axes[0].set_ylabel('Y (m)')
    axes[0].set_title('Sensitivity to Initial Conditions')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].axis('equal')
    
    # Divergence
    axes[1].semilogy(t, divergence, 'g-', linewidth=1)
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Divergence (m)')
    axes[1].set_title('Exponential Divergence (Chaos)')
    axes[1].grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Double Pendulum Visualization Demo")
    print("=" * 50)
    
    # Create pendulum
    pendulum = DoublePendulum(m1=1.0, m2=1.0, L1=1.0, L2=1.0, g=9.81)
    
    # Simulate
    print("Simulating double pendulum...")
    initial_state = np.array([np.pi/2, 0.0, np.pi/2, 0.0])
    t, trajectory = pendulum.simulate(initial_state, (0, 20), num_points=2000)
    
    # Plot analysis
    print("Creating analysis plots...")
    plot_trajectory_analysis(pendulum, t, trajectory, save_path="double_pendulum_analysis.png")
    
    # Create animation (uncomment to generate MP4)
    # print("Creating animation...")
    # animate_pendulum(pendulum, t, trajectory, save_path="double_pendulum.mp4")
    
    # Show animation
    print("Displaying animation...")
    animate_pendulum(pendulum, t, trajectory)
    
    # Compare trajectories to show chaos
    print("\nDemonstrating sensitivity to initial conditions...")
    compare_trajectories(pendulum, (0, 15), num_points=2000, epsilon=0.01)
