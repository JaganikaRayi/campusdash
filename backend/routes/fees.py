from flask import Blueprint, request, jsonify
from backend.services.fee_service import FeeService

fees_bp = Blueprint('fees', __name__, url_prefix='/api')

@fees_bp.route('/fees/<reg_no>', methods=['GET'])
def get_fees(reg_no):
    details = FeeService.get_fee_details(reg_no.upper())
    return jsonify({
        "success": True,
        **details
    })

@fees_bp.route('/fees/pay', methods=['POST'])
def pay_fee():
    data = request.get_json() or {}
    reg_no = data.get('student_reg_no')
    amount = data.get('amount')
    method = data.get('payment_method', 'UPI / NetBanking')

    if not reg_no or not amount:
        return jsonify({"success": False, "message": "Student registration number and amount are required."}), 400

    result = FeeService.process_mock_payment(reg_no.upper(), amount, method)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@fees_bp.route('/reports/fees', methods=['GET'])
def get_fee_report():
    stats = FeeService.get_overall_fee_stats()
    return jsonify({
        "success": True,
        "stats": stats
    })
