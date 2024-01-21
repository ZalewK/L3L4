from L3L4 import app

if __name__ == "__main__":
    with app.app_context():
        BookService.clear_and_initialize_data()
    app.run(debug=True)
