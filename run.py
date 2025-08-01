from app import create_app

# Initialize Flask application
app = create_app()

# Run app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
