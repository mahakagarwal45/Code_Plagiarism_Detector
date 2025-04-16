from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from plagiarism_detector import detect_plagiarism
import os

app = Flask(__name__)
api = Api(app)

class PlagiarismCheck(Resource):
    def post(self):
        try:
            uploaded_file = request.files['user_code']
            filename = uploaded_file.filename

            if not filename:
                return jsonify({"status": "error", "message": "No file uploaded."})

            # Save uploaded file
            user_code_path = os.path.join('uploads', filename)
            uploaded_file.save(user_code_path)

            # Get optional test cases
            test_cases = request.form.get('test_cases') or None

            # Run plagiarism detection
            reference_dir = 'reference_codes/'
            results = detect_plagiarism(user_code_path, reference_dir, test_cases)

            return jsonify({"status": "success", "results": results})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

api.add_resource(PlagiarismCheck, '/codeplag')

if __name__ == '__main__':
    app.run(debug=True)
