from flask import Flask, request, render_template, jsonify

# creating the flask app
app = Flask(__name__)
result = 'initial data'
@app.route("/getData", methods=['POST', 'GET'])
def getInfo():
    if request.method == 'POST':
        global result
        
        text_input = request.get_json()
        print(text_input) 
        result += text_input['data'] 
        return text_input, 200
    else: 
        return result, 200



if __name__ == '__main__':
    app.run(debug=True)
