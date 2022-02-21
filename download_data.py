import os
import json
from tqdm import tqdm
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
from pdf2image import convert_from_path

def read_file(file_path):
    res = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        res.append(line.strip())
    return res

def read_annotation(anno_path):
    with open(anno_path, 'r') as f:
        annos = json.load(f)
    fields = {}
    for fd in annos['Fields']:
        value = fd['value']
        key = fd['key']
        if not value['label'] in fields:
            fields[value['label']] = {}
        # value['label'] corresponds to field label, e.g., invoice date
        # value['tag'] corresponds to field value text, e.g., 01/01/2021
        # value['bbox'] corresponds to the box location of the field value
        # key['tag'] corresponds to key text, e.g., inv date
        # key['bbox'] corresponds to the box location of the key
        fields[value['label']]['text'] = value['tag']
        fields[value['label']]['bbox'] = [value['bbox']['xmin'], value['bbox']['ymin'], value['bbox']['xmax'], value['bbox']['ymax']]
        if key['tag'] is not None:
            fields[value['label']]['key_text'] = key['tag']
            fields[value['label']]['key_bbox'] = [key['bbox']['xmin'], key['bbox']['ymin'], key['bbox']['xmax'], key['bbox']['ymax']]

    return fields

def visualize_annos(args, names):
    for name in tqdm(names):
        image_path = os.path.join(args.out_dir, name+'.png')
        image = Image.open(image_path)
        fig, ax = plt.subplots()
        ax.imshow(image)
        anno_path = os.path.join(args.anno_dir, name+'.json')
        fields = read_annotation(anno_path)
        for fd in fields:
            field_text = fields[fd]['text']
            field_bbox = fields[fd]['bbox']
            rect = patches.Rectangle((field_bbox[0], field_bbox[1]), field_bbox[2]-field_bbox[0],
                                     field_bbox[3]-field_bbox[1], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            ax.text(field_bbox[0], field_bbox[1], fd+': '+field_text, style='italic', size=5)
            if 'key_text' in fields[fd]:
                key_text = fields[fd]['key_text']
                key_bbox = fields[fd]['key_bbox']
                rect = patches.Rectangle((key_bbox[0], key_bbox[1]), key_bbox[2] - key_bbox[0],
                                         key_bbox[3] - key_bbox[1], linewidth=1, edgecolor='b', facecolor='none')
                ax.add_patch(rect)
                ax.text(key_bbox[0], key_bbox[1], fd+': ' + key_text, style='italic', size=5)

        plt.axis('off')
        plt.savefig(os.path.join(args.vis_dir, name+'.png'), dpi=200)
        plt.close()
        plt.clf()

def run_download(names):
    URL_root = 'https://s3-us-west-2.amazonaws.com/edu.ucsf.industrydocuments.artifacts'
    for name in tqdm(names):
        chars = name[0:4]
        char_string = '/'.join([c for c in chars])
        URL = os.path.join(URL_root,char_string, name, name+'.pdf')
        try:
            os.system('wget '+URL+' -P '+os.path.join(args.out_dir, 'tmp/')+' --no-verbose')
            images = convert_from_path(os.path.join(args.out_dir, 'tmp/',name+'.pdf'), dpi=200, last_page=1, fmt='png')
            images[0].save(os.path.join(args.out_dir, name+'.png'))
        except:
            pass
    os.system('rm -r '+os.path.join(args.out_dir, 'tmp/'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', default='labeled')
    parser.add_argument('--anno_dir', default='./annotation')
    parser.add_argument('--out_dir', default='./data')
    parser.add_argument('--vis_dir', default='./vis')
    parser.add_argument('--download', action='store_true', help='download invoice data')
    parser.add_argument('--vis', action='store_true', help='visualize annotations')
    args = parser.parse_args()

    if not args.download and not args.vis:
        raise Exception('at least one of --download and --vis is needed')

    if args.split == 'unlabeled':
        args.name_list_path = 'train_set.txt'
        args.out_dir = os.path.join(args.out_dir, 'unlabeled')
    elif args.split == 'labeled':
        args.name_list_path = 'test_set.txt'
        args.out_dir = os.path.join(args.out_dir, 'labeled')
    else:
        raise NotImplementedError

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    if not os.path.isdir(args.vis_dir):
        os.makedirs(args.vis_dir)

    names = read_file(args.name_list_path)
    if args.download:
        run_download(names)

    if args.vis and args.split == 'labeled':
        visualize_annos(args, names)
