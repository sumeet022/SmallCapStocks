from flask import Flask, render_template, request
import pandas as pd
import Nse1

app = Flask(__name__)

# Sample DataFrame
# data = {
#     'Name': ['Alice', 'Bob', 'Charlie'],
#     'Age': [25, 30, 35]
# }
# df = pd.DataFrame(data)

@app.route('/')
def index(): 
    # Convert the DataFrame to HTML
    dataframe_html = Nse1.generate_dataframe()

    return render_template('index.html',dataframe=dataframe_html.to_html())

@app.route('/get_dataframe')
def get_dataframe():
    # Generate the DataFrame
    dataframe = Nse1.generate_dataframe()
    # Convert DataFrame to JSON
    dataframe_json = dataframe.to_json(orient='records')
    return dataframe_json

if __name__ == '__main__':
    app.run(debug=True)
