import argparse 
import threading
import subprocess
from fastapi import Request
from tools import manager as mg


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--command", type=str, default="", help="the command")
parser.add_argument("-t", "--token", type=str, default="", help="the token")
args = parser.parse_args()

manager = mg.Manager(
    command = args.command,
    token = args.token
)

# The main part
@manager.app.post("/main/{project_uuid}")
@manager.login_required
async def main(request: Request, project_uuid: str):
    finish_flag, _response = manager.labels_prepare(project_uuid)
    main_job()
    if finish_flag:
        return _response
    else:
        return {"message": "Sorry your work isn't done yet.", "finish_flag": False}

def main_job():
    subprocess.run(['python', 'main.py'])
    


if __name__ == "__main__":
    # http://localhost:8000/docs#/
    manager.run(host="0.0.0.0", port=8000)
    




