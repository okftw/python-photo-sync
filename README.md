# python-photo-sync

Script to sync photos from a source path to a destination path based on a date folder structure and naming convention.

The destination file path naming convention is :

```
<Destination Root>/<Year>/<Year Month Day>/<Year Month Day_Hour Minute Second>_<MD5 Checksum>.<Extension>
```

For example :

```
python app.py --source_path D:\Pictures --destination_path E:\Pictures --sync

2021-08-08 03:28:17,673 INFO ------------
2021-08-08 03:28:17,674 INFO Source File               : D:\Pictures\IMG_5077.JPG
2021-08-08 03:28:17,674 INFO Source File Creation Date : 2019-05-22 18:22:48
2021-08-08 03:28:17,698 INFO Source File MD5 Checksum  : 5616e92341e020892c6c73996e93b2ce
2021-08-08 03:28:17,698 INFO
2021-08-08 03:28:17,699 INFO Destination Folder        : E:\Pictures\2019\20190522
2021-08-08 03:28:17,699 INFO Destination File          : E:\Pictures\2019\20190522\20190522_182248_5616E92341E0.JPG
2021-08-08 03:28:17,700 INFO Destination Folder Exists : True
2021-08-08 03:28:17,700 INFO Destination File Exists   : False
2021-08-08 03:28:17,701 INFO Copying File              : D:\Pictures\IMG_5077.JPG --> E:\Pictures\2019\20190522\20190522_182248_5616E92341E0.JPG
2021-08-08 03:28:17,701 INFO ------------
```

Note : 
Running without the `--sync` parameter will do a simulation of what would occur, no directories or files will be created or copied.


```
usage: app.py [-h] [--source_path SOURCE_PATH] [--destination_path DESTINATION_PATH] [--sync]

optional arguments:
  -h, --help            show this help message and exit
  --source_path SOURCE_PATH
                        Source Folder Path
  --destination_path DESTINATION_PATH
                        Destination Folder Path
  --sync                Copy files across
```