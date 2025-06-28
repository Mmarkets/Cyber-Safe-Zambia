from flask import Blueprint, send_file, render_template, request, jsonify
from flask_login import login_required
from weasyprint import HTML
import io
import csv
from datetime import datetime
from models import db  # Assuming db is defined in app.py

report_bp = Blueprint('report', __name__)

@report_bp.route('/api/report/preview', methods=['POST'])
@login_required
def preview_report():
    report_type = request.form.get('report_type')
    date_range = request.form.get('date_range')
    # Mock data for preview
    data = {
        'report_type': report_type,
        'date_range': date_range,
        'data': 'Sample data for preview'
    }
    return jsonify(data)

@report_bp.route('/api/report/download', methods=['GET'])
@login_required
def download_report():
    report_type = request.args.get('report_type')
    date_range = request.args.get('date_range')
    format = request.args.get('format')

    if format == 'pdf':
        # Render HTML template for PDF
        html_content = render_template('reports/threat_summary.html', report_type=report_type, date_range=date_range)
        pdf_file = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)
        return send_file(pdf_file, download_name=f'{report_type}_{datetime.now().strftime("%Y%m%d")}.pdf', as_attachment=True)

    elif format == 'csv':
        # Generate CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Type', 'Severity', 'Timestamp'])
        # Mock data
        writer.writerow([1, 'Phishing', 'High', '2025-06-19 09:00'])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8')), download_name=f'{report_type}_{datetime.now().strftime("%Y%m%d")}.csv', as_attachment=True)