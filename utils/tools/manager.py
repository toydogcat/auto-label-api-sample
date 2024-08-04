import os
import time
import uuid
import yaml
import shutil
import zipfile
from pathlib import Path
from tools import toy
from tools import storehouse as sh
from functools import wraps

from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse, JSONResponse

# from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


class Manager():
    def __init__(self, command = '', token = ''):
        self.storehouse = sh.Storehouse()
        self.version = self.storehouse.version
        self.users = self.storehouse.config['users']
        self.token = self.storehouse.config['token'] if token == '' or token == ' ' else token
        self.command = command
        self.logger = self.storehouse.logger
        self.upload_path = self.storehouse.config['path_home']['upload_path']
        
        self.app = FastAPI()
        self.app.add_middleware(SessionMiddleware, secret_key=self.storehouse.config['secret_key'])
        self.router = APIRouter()
        self.setup_routes()
        self.app.include_router(self.router)
        
        self.logger.info(f"Init the Manager.")
        self.projects_map = {}
        
    def login_required(self, func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            token = request.session.get("token", "Unknown")
            if  token != self.token:
                self.logger.info(f"someone use the wrong token: {token}.")
                raise HTTPException(status_code=401, detail="Authentication required")
            return await func(request, *args, **kwargs)
        return wrapper
    
    def labels_prepare(self, project_uuid: str):
        toy.demo_labels_prepare()
        # check finish or not
        project_root = self.projects_map[project_uuid]['project_root']
        if len(list(project_root.glob(f"*.zip"))) > 0:
            zip_path = list(project_root.glob(f"*.zip"))[0]
            return True, FileResponse(
                zip_path,
                media_type = 'application/zip',
                filename = zip_path.name
            )
        else:
            return False, ""
        
    def setup_routes(self):
        @self.router.post("/")
        async def root_post():
            return {"message": f"Welcome to the auto label server with version: {self.version}"}
        @self.router.get("/")
        async def root_get():
            return {"message": f"Welcome to the auto label server with version: {self.version}"}
        
        @self.router.post("/registration")
        async def registration(item: sh.Item_Login, request: Request):
            if self.token == item.token:
                self.users[item.account] = item.password
                self.logger.info(f"acc: {item.account}, pass: {item.password}, registration.")
                return {"message": f"Registration success."}
            else:
                return {"message": "Your token is wrong."}
        
        @self.router.post("/version")
        @self.login_required
        async def get_version(request: Request):
            acc = request.session.get('account', 'Unknown')
            self.logger.info(f"acc: {acc} get version.")
            return {"message": f"Hello {acc}. Welcome to the auto label server with version: {self.version}"}
        
        @self.router.post("/login")
        async def login(item: sh.Item_Login, request: Request):
            self.logger.info(f"token: {item.token}, acc: {item.account}, pass: {item.password} try to login.")
            if self.token == item.token:
                print(item.account, self.users)
                if item.account in self.users:
                    if self.users[item.account] == item.password:
                        request.session['account'] = item.account
                        request.session['password'] = item.password
                        request.session['token'] = item.token
                        return {"message": f"Welcome {item.account}."}
                    else:
                        return {"message": "Wrong password."}
                else:
                    return {"message": "I can't find you. Please register."}
            else:
                return {"message": "Your token is wrong."}
        
        @self.router.post("/logout")
        async def logout(request: Request):
            if request.session.clear():
                return request.session.clear() 
            return {"message": "Logged out."}

        @self.router.post("/clean_demo_datas")
        @self.login_required
        async def clean_demo_datas():
            toy.clean_demo_datas()
            return {"message": "clean demo datas done!!"}
        
        @self.router.get("/share_image/{image_name}")
        async def get_image(image_name: str, request: Request):
            image_root_path = self.storehouse.config['path_home']['share_images_path']
            image_path = os.path.join(image_root_path, image_name)
            # if not os.path.exists(image_path):
            if Path(image_path).exists():
                raise HTTPException(status_code=404, detail="Image not found")
            
            acc = request.session.get('account', 'Unknown')
            self.logger.info(f"Share image: {image_name} for acc: {acc}.")
            return FileResponse(image_path)

        @self.router.post("/upload_from_zip")
        @self.login_required
        async def upload_from_zip(request: Request, file: UploadFile = File(...)):
            if not file.filename.endswith('.zip'):
                return JSONResponse(content={"message": "File must be a ZIP"}, status_code=400)
            
            # file_location = os.path.join(upload_path, file.filename)
            file_location = Path(self.upload_path).joinpath(file.filename)
            with open(file_location, 'wb+') as file_object:
                shutil.copyfileobj(file.file, file_object)
                
            toy.unzip(file_location)
                
            return {"message": f"Successfully uploaded {file.filename}"}
        
        @self.router.post("/upload_from_url/{url}")
        @self.login_required
        async def upload_from_url(url: str, request: Request):
            file_id = url.split('google.com/file/d/')[1].split('/')[0]
            destination = Path(self.upload_path).joinpath('upload.zip')
            toy.download_file_from_google_drive(file_id, destination)
            time.sleep(3)
            toy.unzip(destination)
            return {"message": f"Successfully download."}
        
        @self.router.post("/inference_labels/{project_name}")
        @self.login_required
        async def inference_labels(request: Request, project_name: str):
            project_root = Path(f'assets/projects/{project_name}')
            images_count = 0
            
            yaml_path = project_root / 'project.yaml'
            with open(yaml_path, 'r') as file:
                yaml_data = yaml.safe_load(file)
            
            # predict inference time
            label_format_list = yaml_data['label_format_list']
            for label_format in label_format_list:
                root_search_path = project_root / label_format['folder_relative_path']
                # common images format
                image_extensions = ['*.jpg', '*.jpeg', '*.png']
                image_files = []
                for ext in image_extensions:
                    image_files.extend(root_search_path.glob(f'**/{ext}'))
                    
                images_count += len(image_files)
                images_count += len(label_format['images_url_list'])
                
            need_all_sec = self.storehouse.config['per_image_cost'] * images_count
            need_hours, remainder = divmod(need_all_sec, 3600)
            need_minutes, need_seconds = divmod(remainder, 60)
            
            # load images from url
            for label_format in label_format_list:
                for image_info in label_format['images_url_list']:
                    img_name = image_info['name']
                    img_type = image_info['type']
                    img_url  = image_info['url']
                    destination = f"assets/projects/{project_name}/{label_format['folder_relative_path']}/{img_name}"
                    if img_type == 'google_drive':
                        img_id = img_url.split('drive.google.com/file/d/')[1].split('/')[0]
                        toy.download_file_from_google_drive(img_id, destination)
                    else:
                        toy.download_file_from_wget(img_url, destination)
            
            project_uuid = str(uuid.uuid1())
            self.projects_map[project_uuid] = {
                'start_time': time.time(),
                'images_count': images_count,
                'predict_time': time.time() + need_all_sec,
                'project_uuid': project_uuid,
                'project_root': project_root,
            }
            output_text = f"{round(need_hours, 1)} hours {round(need_minutes, 1)} minutes {round(need_seconds, 1)} seconds, your project_uuid: {project_uuid}"
            
            return {
                "message": f"Successfully got images count: {images_count}, you need to wait {output_text}",
                "project_uuid": project_uuid,
            }

    def run(self, host = '0.0.0.0', port = 8000):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)



