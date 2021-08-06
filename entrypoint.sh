# ローカル実行時には 以下を実行
# export PORT=2626

# Dockerfile のサーバー起動
export FLASK_APP="server.py"
flask run --host=0.0.0.0 --port=$PORT --with-threads > stdout.log 2> stderr.log
