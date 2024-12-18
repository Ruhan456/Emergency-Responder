from flask import Flask, request, render_template  # Importing necessary modules from Flask
import serial  # Importing serial library to communicate with serial ports

app = Flask(__name__)  # Initializing the Flask application
ser = serial.Serial('COM4', 9600)  # Open serial port COM4 at 9600 baud rate
priority = 0  # Initializing the priority variable, used later to set the priority of a crime report

# Route to display the HTML form at the root URL
@app.route('/')
def index():
    # This function serves the 'index.html' located in the templates folder when the root URL is accessed
    return render_template('index.html')

# Route to handle the submission of the crime report form
@app.route('/submit-crime-report', methods=['POST'])
def submit_crime_report():
    # Extracting data from the form submission using request.form
    crime_category = request.form['crime-category']
    crime_type = request.form['crime-type']
    date_of_crime = request.form['date']
    time_of_crime = request.form['time']
    address = request.form['address']
    number_of_victims = int(request.form['victims'])  # Convert number of victims to an integer
    victim_state = request.form['victim-state']
    statement = request.form['statement']

    # Setting the priority based on the state of the victims
    if victim_state == "Unharmed":
        priority = 0
    elif victim_state == "Injured":
        priority = number_of_victims * 2  # Priority is higher if victims are injured
    elif victim_state == "Deceased":
        priority = number_of_victims * 10  # Highest priority if there are deceased victims

    # Composing a string with crime type, time of crime, and priority and sending it over serial
    ser.write((crime_type + " " + time_of_crime + " " + str(priority) + "\n").encode())

    # Logging the form data to the console, which can be helpful for debugging
    print("Crime Category:", crime_category)
    print("Type of Crime:", crime_type)
    print("Date of Crime:", date_of_crime)
    print("Time of Crime:", time_of_crime)
    print("Address:", address)
    print("Number of Victims:", number_of_victims)
    print("State of Victim(s):", victim_state)
    print("Statement:", statement)

    # Returning a confirmation message after form submission
    return f"Report submitted successfully for {crime_type}"

# Main function to run the application
if __name__ == '__main__':
    try:
        app.run(debug=True)  # Running the Flask app with debugging enabled
    finally:
        ser.close()  # Ensuring the serial connection is closed when the application stops running
