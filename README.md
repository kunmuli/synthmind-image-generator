# Stable Diffusion Image Generator with Amazon Bedrock

## Introduction

This is a Python application that utilizes Streamlit to create a simple user interface for generating images using the Stable Diffusion model with Amazon Bedrock. The generated images are modified based on user prompts.

## Prerequisites

Before running the application, ensure that you have the following installed:

- Python (>=3.6)
- Pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kunmuli/synthmind-image-generator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd synthmind-image-generator
   ```

3. Create a virtual environment (optional but recommended)::

   ```bash
    # On Windows
    python -m venv venv

    # On macOS and Linux
    python3 -m venv venv

   ```

   This will create a virtual environment named venv in your project directory.

4. Activate the virtual environment::

   ```bash
    # On Windows
    .\venv\Scripts\activate

    # On macOS and Linux
    source venv/bin/activate

   ```

   You should see `(venv)` in your terminal prompt, indicating that the virtual environment is active.

5. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory and set the necessary environment variables:

   ```env
   DEBUG=False
   DEFAULT_SEED=12345
   AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
   AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
   AWS_DEFAULT_REGION=us-east-1
   # Add other environment variables as needed
   ```

   Note: Make sure to replace `<your_aws_access_key_id>` and `<your_aws_secret_access_key>` with your actual AWS credentials.

## Running the Application

1. Execute the following command to start the application:

   ```bash
   streamlit run Image_generator.py
   ```

2. Open a web browser and navigate to the provided URL (usually http://localhost:8501) to access the Streamlit app.

## Usage

- Choose the image style and set other parameters in the sidebar.
- Input a prompt in the text box.
- Click the "Generate" button to generate an image based on the prompt.
- View the generated image and download it if needed.

## Additional Information

- The application uses Streamlit to create the user interface, and the image generation is powered by the Stable Diffusion model on Amazon Bedrock.

## License

This project is licensed under the [MIT License](LICENSE).
