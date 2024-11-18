import openai
import re
import matlab.engine

openai.api_key = "YOUR_API_KEY"
openai.api_base = "http://172.31.147.47:4000"

def run_simulink_model(direction, dist, x_pos, y_pos, z_pos):
    # Start MATLAB engine
    x,y,z = 0,0,0
    eng = matlab.engine.start_matlab()

    # Set workspace variables based on input
    eng.load_system('droneSim')
    eng.set_param('droneSim', 'StopTime', dist, nargout=0)
    eng.workspace['x_pos'] = x_pos
    eng.workspace['y_pos'] = y_pos
    eng.workspace['z_pos'] = z_pos

    if direction.lower() == "forward":
        x_pos += float(dist)
        x = 1.0
        y = 0.0
        z = 0.0
    elif direction.lower() == "right":
        y_pos -= float(dist)
        x = 0.0
        y = -1.0
        z = 0.0
    elif direction.lower() == "backward":
        x_pos -= float(dist)
        x = -1.0
        y = 0.0
        z = 0.0
    elif direction.lower() == "left":
        y_pos += float(dist)
        x = 0.0
        y = 1.0
        z = 0.0
    elif direction.lower() == "up":
        z_pos += float(dist)
        x = 0.0
        y = 0.0
        z = 1.0
    elif direction.lower() == "down":
        z_pos -= float(dist)
        x = 0.0
        y = 0.0
        z = -1.0
    else:
        print("Invalid input. Please enter 'W' or 'D'.")
        return


    # Set variables in MATLAB workspace
    eng.workspace['x'] = x
    eng.workspace['y'] = y
    eng.workspace['z'] = z

    eng.sim('droneSim.slx')  # Ensure your model is open or specify full path
    eng.quit()
    return(x_pos,y_pos,z_pos)

def query_llm(user_input):
    # Define the prompt with instructions
    prompt = f"""Extract the direction and distance from the following command: '{user_input}'. The direction has to either be forward, backward, left, right, up, or 
    down(the word has to be exactly one of these, not their synonym). Give the output in the format 'direction,distance' and nothing else."""

    # Query the OpenAI API using the updated method
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with your chosen model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100  # Adjust the token limit as needed
    )
    
    # Extract the model's response
    return response['choices'][0]['message']['content'].strip()

def parse_llm_response(llm_response):

    # Use regex to extract direction and distance
    direction_match = re.search(r'(forward|backward|left|right|up|down)', llm_response, re.IGNORECASE)
    distance_match = re.search(r'(\d+(\.\d+)?)', llm_response)

    direction = direction_match.group(0).lower() if direction_match else None
    distance = float(distance_match.group(0)) if distance_match else None

    return direction, distance

if __name__ == "__main__":
    x_pos, y_pos, z_pos = 0.0,0.0,10.0
    while True:
    # while True:
        user_input = input("Enter command: ")
        if user_input == "exit":
            break;
        response = query_llm(user_input)
        direction, dist = parse_llm_response(response)
        print(direction, dist)
        
        x_pos,y_pos,z_pos = run_simulink_model(direction, str(dist), x_pos, y_pos, z_pos)

