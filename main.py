from website import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1700))
    app.run(debug=False, host='0.0.0.0', port=port)