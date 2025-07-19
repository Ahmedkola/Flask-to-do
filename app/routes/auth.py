from flask import Blueprint, request, session, redirect, url_for, flash, render_template

auth_bp = Blueprint('auth', __name__)

usercredentials = {
    'username': 'admin',
    'password': '1234'   
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == usercredentials['username'] and password == usercredentials['password']:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('task.view_tasks'))  # ✅ redirect after login!
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
