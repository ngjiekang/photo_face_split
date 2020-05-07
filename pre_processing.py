import face_recognition
import os
import pandas as pd
import pickle
from tqdm import tqdm

tqdm.pandas()


def get_face_embedding(file_path):
    img = face_recognition.load_image_file(file_path)
    return face_recognition.face_encodings(img)


def build_df(image_folder_path):
    df = pd.DataFrame()
    df['img_names'] = os.listdir(image_folder_path)
    df['face_encoding'] = df['img_names'].progress_apply(lambda img_name:
                                                         get_face_embedding(
                                                             os.path.join(image_folder_path, img_name)
                                                         ))
    return df

test = ''
path = '../data/weddingphotos{}/'.format(test)
df = build_df(path)
df.to_pickle('../data/wedding_df{}.pickle')
