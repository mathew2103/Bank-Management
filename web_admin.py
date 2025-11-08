from flask import Flask, render_template, request, redirect, url_for, flash
from init import initialize, check_closed

app = Flask(__name__)
app.secret_key = "dev-secret"

cur, db = initialize()

@app.route('/')
def index():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin')
def admin_dashboard():
    if cur is None:
        return "Database not available. Check your SQL credentials in init.py"
    cur.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cur.fetchone()[0]
    return render_template('admin_dashboard.html', total_accounts=total_accounts, total_transactions=total_transactions)

@app.route('/admin/customers')
def customers():
    cur.execute("SELECT accNo, name, balance, IF(closed, 'Yes', 'No') FROM accounts")
    rows = cur.fetchall()
    return render_template('customers.html', customers=rows)

@app.route('/admin/customer/<int:accno>', methods=['GET', 'POST'])
def customer_detail(accno):
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_name':
            name = request.form.get('name')
            cur.execute("UPDATE accounts SET name=%s WHERE accNo=%s", (name, accno))
        elif action == 'update_sec':
            secQ = request.form.get('secQ')
            secA = request.form.get('secA')
            cur.execute("UPDATE accounts SET secQues=%s, secAns=%s WHERE accNo=%s", (secQ, secA, accno))
        elif action == 'close':
            cur.execute("UPDATE accounts SET closed=1 WHERE accNo=%s", (accno,))
        elif action == 'add_money':
            amount = float(request.form.get('amount') or 0)
            cur.execute("UPDATE accounts SET balance=balance+%s WHERE accNo=%s", (amount, accno))
            cur.execute("INSERT INTO notifications (accNo, content) values (%s, %s)", (accno, f"Added {amount}"))
        flash('Action completed.')
        return redirect(url_for('customer_detail', accno=accno))

    cur.execute("SELECT accNo, name, balance, password, secQues, secAns, IF(closed, 'Yes', 'No') FROM accounts WHERE accNo=%s", (accno,))
    acc = cur.fetchone()
    if acc is None:
        return "Account not found", 404
    return render_template('customer_detail.html', acc=acc)

@app.route('/admin/transactions', methods=['GET'])
def transactions():
    cur.execute("SELECT * from transactions order by at desc")
    trs = cur.fetchall()
    return render_template('transactions.html', transactions=trs)

@app.route('/admin/transaction/revert/<int:txid>', methods=['POST'])
def revert_transaction(txid):
    cur.execute("SELECT * from transactions where id=%s", (txid,))
    tr = cur.fetchone()
    if tr is None:
        flash('Transaction not found')
        return redirect(url_for('transactions'))

    amt = tr[4]
    sender = tr[1]
    receiver = tr[2]

    if check_closed(sender, cur, db):
        flash(f"Account number {sender} has been closed. Can't revert transaction!")
        return redirect(url_for('transactions'))
    if check_closed(receiver, cur, db):
        flash(f"Account number {receiver} has been closed. Can't revert transaction!")
        return redirect(url_for('transactions'))

    # perform revert
    cur.execute("UPDATE accounts SET balance=balance-%s where accNo=%s", (amt, receiver))
    cur.execute("UPDATE accounts SET balance=balance+%s where accNo=%s", (amt, sender))
    cur.execute("DELETE from transactions where id=%s", (txid,))
    cur.execute("INSERT INTO notifications (accNo, content) values (%s, %s)", (receiver, f"Transaction reverted! -{amt}"))
    cur.execute("INSERT INTO notifications (accNo, content) values (%s, %s)", (sender, f"Transaction reverted! +{amt}"))

    flash('Transaction reverted')
    return redirect(url_for('transactions'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
