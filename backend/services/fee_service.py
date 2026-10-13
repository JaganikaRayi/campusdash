import uuid
import datetime
from database.db import get_db

class FeeService:
    @staticmethod
    def get_fee_details(student_reg_no):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM fees WHERE student_reg_no = ?", (student_reg_no,))
        fee_row = cursor.fetchone()

        cursor.execute("""
            SELECT * FROM payments
            WHERE student_reg_no = ?
            ORDER BY payment_date DESC, id DESC
        """, (student_reg_no,))
        payments = [dict(p) for p in cursor.fetchall()]

        cursor.execute("SELECT name, email, branch, section FROM students WHERE reg_no = ?", (student_reg_no,))
        student_info = cursor.fetchone()

        conn.close()

        fee_dict = dict(fee_row) if fee_row else {
            "student_reg_no": student_reg_no,
            "total_amount": 75000.0,
            "paid_amount": 0.0,
            "balance_amount": 75000.0
        }

        return {
            "fee_summary": fee_dict,
            "payment_history": payments,
            "student": dict(student_info) if student_info else {}
        }

    @staticmethod
    def process_mock_payment(student_reg_no, amount, payment_method="UPI"):
        conn = get_db()
        cursor = conn.cursor()

        amount = float(amount)
        if amount <= 0:
            conn.close()
            return {"success": False, "message": "Payment amount must be greater than zero."}

        cursor.execute("SELECT * FROM fees WHERE student_reg_no = ?", (student_reg_no,))
        fee_row = cursor.fetchone()
        if not fee_row:
            conn.close()
            return {"success": False, "message": "Fee record not found for this student."}

        current_balance = float(fee_row['balance_amount'])
        if amount > current_balance:
            conn.close()
            return {"success": False, "message": f"Payment amount exceeds outstanding balance of ₹{current_balance:,.2f}"}

        # Generate unique transaction reference and receipt number
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        txn_ref = f"CD-TXN-{int(now.timestamp())}-{uuid.uuid4().hex[:6].upper()}"
        receipt_no = f"REC-{now.year}-{uuid.uuid4().hex[:8].upper()}"

        new_paid = float(fee_row['paid_amount']) + amount
        new_balance = current_balance - amount

        # Update fee record
        cursor.execute("""
            UPDATE fees
            SET paid_amount = ?, balance_amount = ?, last_updated = CURRENT_TIMESTAMP
            WHERE student_reg_no = ?
        """, (new_paid, new_balance, student_reg_no))

        # Record payment
        cursor.execute("""
            INSERT INTO payments (transaction_ref, student_reg_no, amount, payment_date, payment_method, status, receipt_no)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (txn_ref, student_reg_no, amount, date_str, payment_method, 'Successful', receipt_no))

        cursor.execute("SELECT name, email, branch FROM students WHERE reg_no = ?", (student_reg_no,))
        student = dict(cursor.fetchone())

        conn.commit()
        conn.close()

        receipt_data = {
            "receipt_no": receipt_no,
            "transaction_ref": txn_ref,
            "student_reg_no": student_reg_no,
            "student_name": student.get('name'),
            "branch": student.get('branch'),
            "amount": amount,
            "payment_date": date_str,
            "payment_method": payment_method,
            "status": "Successful",
            "balance_remaining": new_balance,
            "total_fee": float(fee_row['total_amount'])
        }

        return {
            "success": True,
            "message": "Payment verified and processed successfully!",
            "receipt": receipt_data
        }

    @staticmethod
    def get_overall_fee_stats():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_students,
                SUM(total_amount) as total_expected,
                SUM(paid_amount) as total_collected,
                SUM(balance_amount) as total_outstanding
            FROM fees
        """)
        stats = dict(cursor.fetchone())
        conn.close()
        return stats
