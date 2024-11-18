import matlab.engine
def run_simulink_model(direction, dist):
    # Start MATLAB engine
    x_pos, y_pos, z_pos = 0.0,0.0,10.0
    
    eng = matlab.engine.start_matlab()

    # Set workspace variables based on input
    eng.load_system('droneSim')
    eng.set_param('droneSim', 'StopTime', dist, nargout=0)
    eng.workspace['x_pos'] = x_pos
    eng.workspace['y_pos'] = y_pos
    eng.workspace['z_pos'] = z_pos

    if direction == "forward" or "Forward":
        x_pos += float(dist)
        x = 1.0
        y = 0.0
    elif direction == "right" or "Right":
        y_pos += float(dist)
        x = 0.0
        y = 1.0
    elif direction == "backward" or "Backward":
        y_pos -= float(dist)
        x = -1.0
        y = 0.0
    elif direction == "left" or "Left":
        y_pos -= float(dist)
        x = 0.0
        y = -1.0
    else:
        print("Invalid input. Please enter 'W' or 'D'.")
        return

    z = 0.0  # z is always set to 0

    # Set variables in MATLAB workspace
    eng.workspace['x'] = x
    eng.workspace['y'] = y
    eng.workspace['z'] = z

    eng.sim('droneSim.slx')  # Ensure your model is open or specify full path
    eng.quit()

# Example usage
# run_simulink_model()