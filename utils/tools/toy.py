import os
import yaml
import shutil
import requests
import subprocess
from pathlib import Path
from sklearn.model_selection import train_test_split


def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_file_from_wget(img_url: str, destination: str):
    # wget -P /home/username/downloads http://example.com/somefile.zip
    subprocess.run(['wget', '-P', destination, img_url])


def unzip(zip_path):
    _path = Path(zip_path)
    name = _path.name.split('.')[0]
    new_path = _path.parent / name
    os.makedirs(str(new_path), exist_ok=True)
    subprocess.run(['unzip', str(zip_path), '-d', str(new_path)])
    
    target_paths = list(new_path.glob('**/project.yaml'))
    for yaml_path in target_paths:
        project_original_path = yaml_path.parent
        with open(yaml_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        project_name = yaml_data['project_name']
        project_destination_path = Path(f'assets/projects/{project_name}')
        
        shutil.move(str(project_original_path), str(project_destination_path))
        print(f"move folder from '{project_original_path}' to '{project_destination_path}'.")

def create_floders(dest_root_path: Path):
    (dest_root_path / 'train' / 'images').mkdir(parents=True, exist_ok=True)
    (dest_root_path / 'train' / 'labels').mkdir(parents=True, exist_ok=True)
    (dest_root_path / 'valid' / 'images').mkdir(parents=True, exist_ok=True)
    (dest_root_path / 'valid' / 'labels').mkdir(parents=True, exist_ok=True)
    (dest_root_path / 'test' / 'images').mkdir(parents=True, exist_ok=True)
    (dest_root_path / 'test' / 'labels').mkdir(parents=True, exist_ok=True)

def label_get_name(label_path: Path):
    return label_path.name.rsplit('.', 1)[0]

def image_get_path_form_label(label_path: Path):
    name = label_get_name(label_path)
    path = label_path.parents[1] / 'images'
    path.glob(f"{name}.*")
    return list(path.glob(f"{name}.*"))[0]

def copy_label(label_path: Path, dest_root_path: Path, data_type: str):
    name = label_get_name(label_path)
    _dest = dest_root_path / data_type / 'labels' / f"{name}.txt"
    shutil.copyfile(label_path, _dest) 

def copy_image(label_path: Path, dest_root_path: Path, data_type: str):
    name = label_get_name(label_path)
    image_path = image_get_path_form_label(label_path)
    _dest = dest_root_path / data_type / 'images' / image_path.name
    shutil.copyfile(image_path, _dest) 

def clean_demo_datas():
    command = f'rm -rf "./assets/projects/demo_sample"'
    subprocess.run(command, shell = True, capture_output = True, text = True)
    command = f'rm -rf "./assets/upload_home/demo_input"'
    subprocess.run(command, shell = True, capture_output = True, text = True)
    command = f'rm -f "./assets/upload_home/demo_input.zip"'
    subprocess.run(command, shell = True, capture_output = True, text = True)

def demo_labels_prepare():
    dest_root_path = Path('./assets/projects/demo_sample')
    orig_path_root = Path('./utils/datas/all_label_datas')
    # check do it or not
    if Path(dest_root_path / 'data.yaml').exists():
        return True
    shutil.copyfile(orig_path_root / 'data.yaml', dest_root_path / 'data.yaml') 
    create_floders(dest_root_path)

    # splite datas
    path_labels = orig_path_root / 'labels'
    path_labels_list = list(path_labels.glob('*.txt'))
    path_labels_train, path_labels_rest = train_test_split(path_labels_list, test_size=0.15, random_state=87)
    path_labels_validation, path_labels_test = train_test_split(path_labels_rest, test_size=0.3, random_state=87)
    # train datas
    for path in path_labels_train:
        copy_label(path, dest_root_path, 'train')
        copy_image(path, dest_root_path, 'train')
    # valid datas
    for path in path_labels_validation:
        copy_label(path, dest_root_path, 'valid')
        copy_image(path, dest_root_path, 'valid')
    # test datas
    for path in path_labels_test:
        copy_label(path, dest_root_path, 'test')
        copy_image(path, dest_root_path, 'test')
        
    shutil.copyfile('./utils/datas/demo_datas/demo_output.zip', dest_root_path / 'demo_output.zip')
    return True
    



    