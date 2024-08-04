import argparse 
import subprocess

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--method", type=str, default="backend", help="backend or client.")
parser.add_argument("-c", "--command", type=str, default="", help="the command")
parser.add_argument("-t", "--token", type=str, default="", help="the token")
parser.add_argument("-ct", "--check_type", type=str, default="new_one", help="the check type, new_one, demo_inference, demo_inference_url, demo_clean or test")
parser.add_argument("-pu", "--project_uuid", type=str, default="", help="the project uuid")
args = parser.parse_args()

def main():
    if args.method == 'backend' or args.method == 'b':
        subprocess.run(['python', 'utils/backend.py', f"-c {args.command}", f"-t {args.token}"])
    elif args.method == 'client' or args.method == 'c':
        command_list = ['python', 'utils/client.py', "--check_type", args.check_type]
        if args.project_uuid != "":
            command_list.append(["--project_uuid", args.project_uuid])
        subprocess.run(command_list)
    else:
        pass

if __name__ == "__main__":
    main()