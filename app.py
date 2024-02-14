from flask import Flask, request, render_template
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def calculate_roots(a, b, c):
    x = sp.symbols('x')
    equation = sp.Eq(a*x**2 + b*x + c, 0)
    roots = sp.solve(equation, x)
    return roots

def plot_graph(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a*x**2 + b*x + c
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Quadratic Equation Graph')
    plt.grid(True)
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graph_url

@app.route('/', methods=['GET', 'POST'])
def quadratic():
    if request.method == 'POST':
        a = float(request.form['a'])
        b = float(request.form['b'])
        c = float(request.form['c'])
        
        equation_str = f"{a}x^2 "
        if b >= 0:
            equation_str += "+ "
        else:
            equation_str += "- "
        equation_str += f"{abs(b)}x "
        if c >= 0:
            equation_str += "+ "
        else:
            equation_str += "- "
        equation_str += f"{abs(c)} = 0"
        
        roots = calculate_roots(a, b, c)
        
        if 'plot' in request.form:
            graph_url = plot_graph(a, b, c)
            return render_template('index.html', equation=equation_str, roots=roots, plot=True, graph_url=graph_url)
        else:
            return render_template('index.html', equation=equation_str, roots=roots, plot=False)
        
    return render_template('index.html', equation=None, roots=None, plot=False)

if __name__ == '__main__':
    app.run(debug=True)
