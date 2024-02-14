from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sum', methods=['POST'])
def calculate_sum():
    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])
    result = num1 + num2
    return jsonify({'result': result})

@app.route('/plot', methods=['POST'])
def plot():
    # Generate 50 random numbers
    x = np.arange(1, 51)
    y = np.random.rand(50)
    
    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.xlabel('Index')
    plt.ylabel('Random Number')
    plt.title('Plot of 50 Random Numbers')
    
    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode plot image as base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    plt.close()
    
    return jsonify({'plot_url': plot_url})

if __name__ == '__main__':
    app.run(debug=True)
