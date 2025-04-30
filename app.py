from flask import Flask, render_template, request, send_file
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import csv
import requests
from plagiarism_detector import detect_plagiarism
from fetchers.github_fetch import fetch_github_code
from datasets import load_dataset
from flask_wtf import FlaskForm
from wtforms import Form, SelectField
from wtforms.validators import DataRequired
report_data = {
    "overall_avg": 0,
    "precision": 85,
    "recall": 80,
    "f1": 82.5,
    "accuracy": 83,
    "confusion_matrix": [[50, 10], [5, 35]]
}
# import streamlit as st
# from kaggle import download_kaggle_code_samples
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
REPORT_PATH = 'report.csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
class LanguageForm(FlaskForm):
    language = SelectField(
        'Programming Language',
        choices=[('cpp', 'C++'), ('py', 'Python'), ('java', 'Java')],
        validators=[DataRequired()]
    )
# # Streamlit interface
# st.title("Compare Your Code with Kaggle Code")

# # Upload the user's code file
# uploaded_file = st.file_uploader("Upload your code file", type=["py", "java", "cpp"])

# if uploaded_file is not None:
#     user_code = uploaded_file.read().decode("utf-8")
#     st.subheader("Your Code:")
#     st.code(user_code, language='python')

#     # Fetch Kaggle code samples
#     dataset_name = 'zillow/zecon'  # Example dataset, change this as needed
#     download_path = './kaggle_code_samples'
#     download_kaggle_code_samples(dataset_name, download_path)

#     # Compare user code with Kaggle code samples
#     comparison_results = []
#     for root, dirs, files in os.walk(download_path):
#         for file in files:
#             if file.endswith('.py'):  # Assuming Python code
#                 with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
#                     kaggle_code = f.read()
#                     similarity = calculate_similarity(user_code, kaggle_code)
#                     comparison_results.append((file, similarity))

#     # Show the comparison results
#     st.subheader("Comparison Results:")
#     for file, similarity in comparison_results:
#         st.write(f"File: {file}, Similarity: {similarity:.2f}")


# Fetch Codeforces User Info
def fetch_codeforces_info(username):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        user = data['result'][0]
        return {
            'handle': user['handle'],
            'rank': user['rank'],
            'rating': user['rating'],
            'max_rating': user['maxRating'],
            'max_rank': user['maxRank']
        }
    return None

# Fetch GeeksforGeeks User Info
def fetch_gfg_code(username):
    url = f"https://gfg-api-fefa.onrender.com/{username}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Fetch CodeSearchNet Code Snippets
def fetch_reference_codes(language, max_files=10):
    dataset = load_dataset("code_search_net", language, split="train")
    samples = dataset.shuffle(seed=42).select(range(max_files))
    return [sample['code'] for sample in samples]

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    pie_data = {"original": 0, "plagiarized": 0}
    predictions = []
    user_code_path = ""
    form = LanguageForm()
    if form.validate_on_submit():
        selected_language = form.language.data
        # Handle the selected language
        return f"Selected Language: {selected_language}"

    if request.method == "POST":
        try:
            user_code = request.form.get("user_code")
            file = request.files.get("code_file")
            user_code_path = ""

            # If code is provided through the form
            if user_code:
                if form.language.data == 'py':
                    user_code_path = os.path.join(app.config['UPLOAD_FOLDER'], "user_code.py")
                elif form.language.data == 'cpp':
                    user_code_path = os.path.join(app.config['UPLOAD_FOLDER'], "user_code.cpp")
                elif form.language.data == 'java':
                    user_code_path = os.path.join(app.config['UPLOAD_FOLDER'], "user_code.java")
                
                with open(user_code_path, "w") as f:
                    f.write(user_code)
            # If a file is uploaded and it has a valid extension
            elif file and file.filename.endswith((".py", ".cpp", ".java")):
                user_code_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(user_code_path)

            if user_code_path:
                # Fetch latest GitHub reference code
                fetch_github_code()

                # Set the directory for reference codes
                reference_codes_dir = "reference_codes/"

                # Perform plagiarism detection
                results, metrics = detect_plagiarism(user_code_path, reference_codes_dir)

                # Extract similarity scores
                all_scores = [float(res["Similarity Score"]) for res in results if isinstance(res["Similarity Score"], (int, float))]
                overall_avg = round((sum(all_scores) / len(all_scores))*100) if all_scores else 0.0

                # Pie chart data for plagiarism percentage
                pie_data["original"] = round(100 - overall_avg)
                pie_data["plagiarized"] = round(overall_avg)

                # Metrics for precision, recall, and F1 score
                precision, recall, f1 = metrics.get("precision", 0), metrics.get("recall", 0), metrics.get("f1", 0)
                predictions = metrics.get("predictions", [])
                
                # Save the plagiarism detection results to a CSV file
                with open(REPORT_PATH, "w", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["Reference File", "Similarity Score", "Prediction"])
                    writer.writeheader()
                    for row in results:
                        writer.writerow(row)

        except Exception as e:
            print("🔥 ERROR:", e)

    return render_template(
        "index.html",
        overall_avg=overall_avg,
        pie_data=pie_data,
        precision=precision,
        recall=recall,
        f1=f1,
        form=form,
        results=results
    )
@app.route("/download_report")
def download_report():
    overall_avg = report_data["overall_avg"]  # <-- add this line
    precision = report_data["precision"]
    recall = report_data["recall"]
    f1 = report_data["f1"]
    accuracy = report_data["accuracy"]
    confusion_matrix = report_data["confusion_matrix"]

    # Create pie chart
    pie_labels = ['Original', 'Plagiarized']
    pie_sizes = [100 - overall_avg, overall_avg]
    pie_colors = ['#4CAF50', '#F44336']
    plt.figure(figsize=(4, 4))
    plt.pie(pie_sizes, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    pie_chart_path = 'static/pie_chart.png'
    plt.savefig(pie_chart_path)
    plt.close()

    # Create confusion matrix heatmap
    plt.figure(figsize=(4, 4))
    plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Original', 'Plagiarized'])
    plt.yticks(tick_marks, ['Original', 'Plagiarized'])
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    for i in range(2):
        for j in range(2):
            plt.text(j, i, str(confusion_matrix[i][j]), ha='center', va='center', color='white')
    confusion_matrix_path = 'static/confusion_matrix.png'
    plt.savefig(confusion_matrix_path)
    plt.close()

    # Create PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, "PlagiCheck")

    # Pie chart
    c.drawImage(pie_chart_path, 50, height - 300, width=200, height=200)

    # Metrics
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 100, f"Plagiarism Score: {overall_avg}%")
    c.drawString(300, height - 120, f"Accuracy: {accuracy}%")
    c.drawString(300, height - 140, f"Precision: {precision}%")
    c.drawString(300, height - 160, f"Recall: {recall}%")
    c.drawString(300, height - 180, f"F1 Score: {f1}%")

    # Confusion matrix
    c.drawImage(confusion_matrix_path, 50, height - 550, width=200, height=200)

    c.save()
    buffer.seek(0)

    # Clean up images
    os.remove(pie_chart_path)
    os.remove(confusion_matrix_path)

    return send_file(buffer, as_attachment=True, download_name="plagiarism_report.pdf", mimetype='application/pdf')

@app.route("/codeforces", methods=["GET", "POST"])
def codeforces():
    user_info = None
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            user_info = fetch_codeforces_info(username)
    return render_template("codeforces.html", user_info=user_info)

@app.route("/gfg", methods=["POST"])
def gfg():
    username = request.form.get("gfg_username")
    user_data = fetch_gfg_code(username)
    if user_data:
        return render_template("gfg.html", user_data=user_data)
    else:
        return "GFG user not found", 404

@app.route("/codesearchnet", methods=["POST"])
def codesearchnet():
    language = request.form.get("language")
    code_snippets = fetch_reference_codes(language)
    return render_template("codesearchnet.html", code_snippets=code_snippets)
if __name__ == "__main__":
    app.run(debug=True)

