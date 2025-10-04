# Circular Display App

A Slint frontend application with Python backend that displays a black screen optimized for a 240x240 circular display.

## Prerequisites

You need to install Python and the required dependencies:

1. **Install Python**: Download from [https://python.org/](https://python.org/) (Python 3.8+ recommended)
2. **Verify Installation**: Open a terminal and run:
   ```bash
   python --version
   pip --version
   ```

## Running the Application

1. **Install Python Dependencies**: Run the following command in the project directory:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py` - Python backend that runs the Slint frontend
- `main.slint` - Slint UI definition with black screen for 240x240 display
- `requirements.txt` - Python dependencies

## Features

- **Python Backend**: Easy to extend with additional logic
- **Slint Frontend**: High-performance UI optimized for embedded displays
- **240x240 Resolution**: Perfect for circular displays
- **Black Background**: Clean, minimal appearance
- **Cross-platform**: Works on Windows, macOS, and Linux

## Backend Development

The Python backend (`main.py`) is where you can add:
- Data processing logic
- API integrations
- Business logic
- Hardware interface code
- Sensor data handling

## Frontend Customization

To modify the display, edit the `main.slint` file. The current configuration creates a simple black screen that's perfect for circular displays.

## Architecture

- **Frontend**: Slint UI (240x240 black screen)
- **Backend**: Python (main.py)
- **Integration**: Slint Python bindings
