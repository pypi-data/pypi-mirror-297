import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import zipfile
import shutil
from lxml import etree as ET
import tempfile
from distutils.dir_util import copy_tree

def change_extension(path, filename, ext):
    pre, old = os.path.splitext(filename)
    os.rename(path + "/" + filename, path + "/" + pre + ext)

def cbz_to_zip(path):
    chapters = [f for f in listdir(path) if isfile(join(path, f))]
    if all(file.endswith('.cbz') for file in chapters):
        for chapter in chapters:
            change_extension(path, chapter, ".zip")

def extract_zips(path, output):
    counter = 1
    zips = [f for f in listdir(path) if isfile(join(path, f))]
    for file in zips:
        with zipfile.ZipFile(os.path.join(path, file), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(output, str(counter)))
        counter += 1

def rename_jpgs(path):
    outchapters = listdir(path)
    prevcounter = 0
    for directory in outchapters:
        pngpath = os.path.join(path, directory)
        pngs = listdir(pngpath)

        if prevcounter == 0:
            prevcounter = len(pngs) - 1
        else:
            os.remove(os.path.join(pngpath, "ComicInfo.xml"))
            pngs.pop()
            for index, filename in enumerate(pngs):
                file_extension = os.path.splitext(filename)[1]
                new_filename = f"{'000' + str(index + prevcounter + 1)}{file_extension}"

                old_file_path = os.path.join(pngpath, filename)
                new_file_path = os.path.join(pngpath, new_filename)
                os.rename(old_file_path, new_file_path)

            files = os.listdir(pngpath)
            for filename in files:
                new_filename = filename.replace('000', '')

                old_file_path = os.path.join(pngpath, filename)
                new_file_path = os.path.join(pngpath, new_filename)

                os.rename(old_file_path, new_file_path)
            prevcounter += len(pngs)

def combine_chapters(input_path, output_path):
    for directory in listdir(input_path):
        shutil.copytree(os.path.join(input_path, directory), output_path, dirs_exist_ok=True)

def mod_xml(path, volume_name, series_name):
    pages = len(listdir(path))
    xmlpath = os.path.join(path, "ComicInfo.xml")
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    title = root.find('Title')
    series = root.find('Series')
    page_count = root.find('PageCount')

    if title is not None:
        title.text = volume_name
    if series is not None:
        series.text = series_name
    if page_count is not None:
        page_count.text = str(pages - 1)

    tree.write(xmlpath, pretty_print=True, encoding='utf-8', xml_declaration=True)

def make_archive(input_path, output_path, volume_name):
    shutil.make_archive(os.path.join(input_path, str(volume_name)), 'zip', output_path)

def combine_files(inpath, volume_title, series_title, m=False):
    inpath = str(inpath)

    print("Copying files to a temp directory...")
    temp_main = tempfile.TemporaryDirectory().name
    copy_tree(inpath, temp_main)

    if m:
        title = volume_title
        counter = 1
        for folder in os.listdir(temp_main):
            volume_title = title + str(counter)
            print("VOLUME " + str(counter))

            print("Changing .cbz to .zip...")
            cbz_to_zip(os.path.join(temp_main, folder))

            print("Extracting pages...")
            outpath = os.path.join(temp_main, folder, "output")
            Path(outpath).mkdir(parents=True, exist_ok=True)
            extract_zips(os.path.join(temp_main, folder), outpath)

            print("Reorganizing pages...")
            rename_jpgs(outpath)

            print("Combining chapters...")
            resultpath = os.path.join(temp_main, folder, "result")
            Path(resultpath).mkdir(parents=True, exist_ok=True)
            combine_chapters(outpath, resultpath)

            print("Modyfing xml data...")
            mod_xml(resultpath, volume_title, series_title)

            print("Finalizing...")
            make_archive(inpath, resultpath, volume_title)
            change_extension(inpath, volume_title + ".zip", ".cbz")

            print("Done! Files in " + str(os.path.join(inpath, folder)) + " combined into a single file " + volume_title + ".cbz")
            counter+=1
    else:

            print("Copying files to a temp directory...")
            copy_tree(inpath, temp_main)

            print("Changing .cbz to .zip...")
            cbz_to_zip(temp_main)

            print("Extracting pages...")
            outpath = os.path.join(temp_main, "output")
            Path(outpath).mkdir(parents=True, exist_ok=True)
            extract_zips(temp_main, outpath)

            print("Reorganizing pages...")
            rename_jpgs(outpath)

            print("Combining chapters...")
            resultpath = os.path.join(temp_main,"result")
            Path(resultpath).mkdir(parents=True, exist_ok=True)
            combine_chapters(outpath, resultpath)

            print("Modyfing xml data...")
            mod_xml(resultpath, volume_title, series_title)

            print("Finalizing...")
            make_archive(inpath, resultpath, volume_title)

            print("Changing extension...")
            change_extension(inpath, volume_title + ".zip", ".cbz")

            print("Done! Files in " + inpath + " combined into a single file " + volume_title + ".cbz")