## Marketing Multi-Agent System for Finding Healthcare Providers

This project uses CrewAI to build a marketing multi-agent system that can surf the internet and find healthcare providers similar to a provider given by the user. The search is based on criteria such as specialty, location, and other parameters mentioned by the user. The application includes a user interface built with Gradio.

## Features

- Multi-agent system using CrewAI
- Searches the internet for healthcare providers
- User-defined search criteria: specialty, location, etc.
- User interface built with Gradio
- Easy to run with a single command

## Installation

### Prerequisites

Make sure you have Python installed. This project is compatible with Python 3.10+.

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/mudit14224/marketing_multiagents.git
    cd marketing_multiagents
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

After installing the necessary libraries, you can run the application with:

    ```bash
    python app.py
    ```

This command will start the Gradio user interface, allowing you to input your search criteria and find healthcare providers based on your specifications.

## Usage

1. Open the application by running `python app.py`.
2. A Gradio user interface will appear.
3. Input the details of the healthcare provider you are looking for, such as:
   - Url of the healthcare provider website
   - Specialty
   - Location
   - Other relevant criteria
5. The multi-agent system will search the internet and display a list of similar healthcare providers based on your criteria.

## Project Structure

- `app.py`: Main application script that initializes and runs the Gradio interface.
- `requirements.txt`: List of required libraries and dependencies.
- `README.md`: This file, providing an overview of the project and instructions for installation and usage.

## Requirements

The `requirements.txt` file includes the necessary libraries to run this project. Make sure to install them using the `pip install -r requirements.txt` command.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any inquiries or feedback, please contact [muditjindal2025@u.northwestern.edu].

---

By following the steps outlined above, you will be able to set up and run the marketing multi-agent system for finding healthcare providers with ease. Enjoy using the application!
