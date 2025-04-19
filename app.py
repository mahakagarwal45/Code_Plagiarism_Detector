from flask import Flask, render_template, request, send_file, jsonify
import os
import csv
from plagiarism_detector import detect_plagiarism

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
REPORT_PATH = 'report.csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    avg_scores = {}
    overall_avg = 0
    precision = recall = f1 = 0
    pie_data = {"original": 0, "plagiarized": 0}
    predictions = []
    user_code_path = ""

    if request.method == "POST":
        try:
            user_code = request.form.get("user_code")
            file = request.files.get("code_file")
            user_code_path = ""

            if user_code:
                user_code_path = os.path.join(app.config['UPLOAD_FOLDER'], "user_code.py")
                with open(user_code_path, "w") as f:
                    f.write(user_code)
            elif file and file.filename.endswith((".py", ".cpp", ".java")):
                user_code_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(user_code_path)

            if user_code_path:
                reference_codes_dir = "reference_codes/"
                results, metrics = detect_plagiarism(user_code_path, reference_codes_dir)

                all_scores = [float(res["Similarity Score"]) for res in results if isinstance(res["Similarity Score"], (int, float))]
                overall_avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0.0

                pie_data["original"] = round(100 - overall_avg, 2)
                pie_data["plagiarized"] = round(overall_avg, 2)

                precision, recall, f1 = metrics["precision"], metrics["recall"], metrics["f1"]
                predictions = metrics["predictions"]
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
        f1=f1
    )

@app.route("/download_report")
def download_report():
    return send_file(REPORT_PATH, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
