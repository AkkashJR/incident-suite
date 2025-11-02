from flask import Flask, jsonify, request
from flask_cors import CORS

from cleanup import cleanup_disk
from unlock_account import unlock_user
from logcollection import collect_and_email_logs
from systemsnapshot import collect_system_info
from installer import install_all_softwares
from selfheal import self_heal_system
from compliance_check import run_compliance_check


app = Flask(__name__)
CORS(app)

@app.route('/api/disk_cleanup', methods=['GET', 'POST'])
def disk_cleanup_route():
    result = cleanup_disk()
    return jsonify({"status": "success", "message": result})

@app.route('/api/unlock_account', methods=['POST'])
def unlock_account_route():
    data = request.get_json()
    username = data.get("username")
    result = unlock_user(username)
    return jsonify({"status": "success", "message": result})

@app.route('/api/logs', methods=['POST'])
def logs_route():
    result = collect_and_email_logs()
    return jsonify({"status": "success", "message": result})

@app.route('/api/system_snapshot', methods=['POST'])
def system_snapshot_route():
    result = collect_system_info()
    return jsonify({"status": "success", "message": result})

@app.route('/api/install_softwares', methods=['POST'])
def install_softwares_route():
    result = install_all_softwares()
    return jsonify({"status": "success", "message": result})

@app.route('/api/self_heal', methods=['POST'])
def self_heal_route():
    result = self_heal_system()
    return jsonify({"status": "success", "message": result})

@app.route('/api/compliance_check', methods=['POST'])
def compliance_check_route():
    result = run_compliance_check()
    return jsonify({"status": "success", "message": result})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)