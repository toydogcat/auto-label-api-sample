
# Explain
```python
# label project object 
label_format_data = {
    'project_name': "demo_sample",
    'output_type': "label",       # 'enum': ['label', 'yolov5', 'yolov7', 'yolov8']
    'label_format_list': [ label_format_obj, ...]
}

# label object
label_format_obj = {
    'folder_relative_path' : 'local_image_path',
    'images_url_list': [ image_url_obj, ...],
    'prompt_list': ['dumbbell', 'people'],
    'prompt_map_list': [ prompt_map_obj, ...], 
}

image_url_obj = {
    'name': 'image name',
    'url': 'url path',
    'type': 'google_drive',     # 'enum': ['google_drive', 'wget']
}

prompt_map_obj = {
    'label_name': '01-2kg',
    'label_index_level': 0,
    'prompt_index': 0,
    'use_flag': True,
}
```

* label_index_level for yolo label order
* If the levels are the same, use dictionary sorting

label_index_level 是給最後yolo標記的順序使用，如果有兩個同等級不同名字字的標記就使用字典排序，假設有三個標記名，啞鈴2kg(label_index_level=1), 啞鈴4kg(label_index_level=1), 跑鞋(label_index_level=0)，則最後輸出的標記順序為．

0. 跑鞋
1. 啞鈴2kg
2. 啞鈴4kg


# Sample
```yaml
label_format_list:
- folder_relative_path: images/2kg
  images_url_list:
  - name: IMG_6294_jpg.rf.06971cb7130ce35d3cf6d9959f1b3505.jpg
    type: google_drive
    url: https://drive.google.com/file/d/17xWPCNgFbV8jpiXcylxa-8ZyaTsBpb0S/view?usp=drive_link
  - name: IMG_6286_jpg.rf.9d5ef28e07045d30e5ad477f476d8eaf.jpg
    type: google_drive
    url: https://drive.google.com/file/d/1rp67OGeuh58cKAqhb4w7Iim8OJkMson1/view?usp=drive_link
  - name: IMG_6288_jpg.rf.cc85bdf856af273b157fcaf7d201a1e4.jpg
    type: google_drive
    url: https://drive.google.com/file/d/12VYp3Ty3W77dSzPPlTxh1RxcRRPAv5uC/view?usp=drive_link
  - name: IMG_6294_jpg.rf.06971cb7130ce35d3cf6d9959f1b3505.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_2kg_6294_jpg.rf.06971cb7130ce35d3cf6d9959f1b3505.jpg
  - name: IMG_6296_jpg.rf.b68bdbe894696fcbe9fd000bdf95a634.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_2kg_6296_jpg.rf.b68bdbe894696fcbe9fd000bdf95a634.jpg
  - name: IMG_6299_jpg.rf.e17497d668a69d0c2d3bc1695a876dfe.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_2kg_6299_jpg.rf.e17497d668a69d0c2d3bc1695a876dfe.jpg
  prompt_list:
  - dumbbell
  - people
  prompt_map_list:
  - label_index_level: 0
    label_name: 01-2kg
    prompt_index: 0
    use_flag: true
  - label_index_level: 0
    label_name: 01-2kg
    prompt_index: 1
    use_flag: false
- folder_relative_path: images/4kg
  images_url_list:
  - name: IMG_6256_jpg.rf.aef64f2d57453a5c4b3df02d19d9ca49.jpg
    type: google_drive
    url: https://drive.google.com/file/d/1vC7L4QdokIaCjCIb4Sm7maX1ljfNzBQ0/view?usp=drive_link
  - name: IMG_6260_jpg.rf.0649ab8a23175195cb9496d9a5025878.jpg
    type: google_drive
    url: https://drive.google.com/file/d/1UBD-DfNo7EyX6ypRlW1_qsxElh2YIToB/view?usp=drive_link
  - name: IMG_6273_jpg.rf.6732ffb8567b7963be3f9304d20990f3.jpg
    type: google_drive
    url: https://drive.google.com/file/d/1_YIWn9XUdmC8HjdQsaXCl24fjezkVqVv/view?usp=drive_link
  - name: IMG_6278_jpg.rf.d298eb52fd5206a130555324d533ebb8.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_4kg_6278_jpg.rf.d298eb52fd5206a130555324d533ebb8.jpg
  - name: IMG_6477_jpg.rf.ff2e1f6782c0d97803140ceb96bf4863.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_4kg_6477_jpg.rf.ff2e1f6782c0d97803140ceb96bf4863.jpg
  - name: IMG_6480_jpg.rf.0c2858855385eb66660864e64360e1fc.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_4kg_6480_jpg.rf.0c2858855385eb66660864e64360e1fc.jpg
  prompt_list:
  - dumbbell
  prompt_map_list:
  - label_index_level: 1
    label_name: 02-4kg
    prompt_index: 0
    use_flag: true
- folder_relative_path: images/6kg
  images_url_list:
  - name: IMG_6326_jpg.rf.b9b786e74ab9c1f3ff0df1119e8b0c48.jpg
    type: google_drive
    url: https://drive.google.com/file/d/1lh_Semf3kCuQfK9FLgLcaSe9an7CEXph/view?usp=drive_link
  - name: IMG_6331_jpg.rf.4fa88c70844bed36ba6dd6d3ed1d5217.jpg
    type: google_drive
    url: https://drive.google.com/file/d/11-GOdcKJEWSdJEGoI54zg6vjXSgCEXnq/view?usp=drive_link
  - name: IMG_6353_jpg.rf.1a45fd977056e36030099700a00c7dbc.jpg
    type: google_drive
    url: https://drive.google.com/file/d/1TLoFX5YxGbqzjELIIFr7kWAjtS6zmAgc/view?usp=drive_link
  - name: IMG_6355_jpg.rf.664ae1dd08a6deb0ca59a4fabb3be163.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_6kg_6355_jpg.rf.664ae1dd08a6deb0ca59a4fabb3be163.jpg
  - name: IMG_6359_jpg.rf.df69b7ab1c82f990468bf17d898ba0d9.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_6kg_6359_jpg.rf.df69b7ab1c82f990468bf17d898ba0d9.jpg
  - name: IMG_6580_jpg.rf.5a352e72aef12242aa02baea63b311ff.jpg
    type: wget
    url: http://localhost:8000/share_image/IMG_6kg_6580_jpg.rf.5a352e72aef12242aa02baea63b311ff.jpg
  prompt_list:
  - dumbbell
  prompt_map_list:
  - label_index_level: 2
    label_name: 03-6kg
    prompt_index: 0
    use_flag: true
output_type: label
project_name: demo_sample
```

# Json Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "label_format_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "folder_relative_path": {
            "type": "string"
          },
          "images_url_list": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "type": {
                  "type": "string",
                  "enum": ["google_drive", "wget"]
                },
                "url": {
                  "type": "string",
                  "format": "uri"
                }
              },
              "required": ["name", "type", "url"]
            }
          },
          "prompt_list": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "prompt_map_list": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "label_index_level": {
                  "type": "integer",
                  "minimum": 0
                },
                "label_name": {
                  "type": "string"
                },
                "prompt_index": {
                  "type": "integer",
                  "minimum": 0
                },
                "use_flag": {
                  "type": "boolean"
                }
              },
              "required": ["label_index_level", "label_name", "prompt_index", "use_flag"]
            }
          }
        },
        "required": ["folder_relative_path", "images_url_list", "prompt_list", "prompt_map_list"]
      }
    },
    "output_type": {
      "type": "string",
      "enum": ["label", "yolov5", "yolov7", "yolov8"]
    },
    "project_name": {
      "type": "string"
    }
  },
  "required": ["label_format_list", "output_type", "project_name"]
}
```

