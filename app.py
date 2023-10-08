from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/post', methods=['POST'])
def receive_post_request():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        # You can access the JSON data as a Python dictionary
        # For example, if the JSON contains a "message" field:
        message = data.get('message', 'No message provided')
        return jsonify({'received_message': message})
    else:
        return jsonify({'error': 'Invalidi JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
