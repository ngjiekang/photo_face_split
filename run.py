import face_recognition
import os
import pandas as pd
import pickle
from itertools import chain
import networkx as nx

# references
# https://github.com/ageitgey/face_recognition/issues/359
# kiv
# from chinese_whispers import chinese_whispers
# chinese_whispers(G, weighting='top', iterations=20)

test = ''
pickle_path = '../data/wedding_df{}.pickle'.format(test)
df = pd.read_pickle(pickle_path)

df['num_faces'] = df['face_encoding'].apply(lambda x: len(x))
total_num_faces = sum(df['num_faces'])
print('total_num_faces', total_num_faces)

count, face_ids_list = 0, []
for i, v in enumerate(df['num_faces']):
    face_ids_list.append(list(range(count, count + v)))
    count += v
df['face_ids'] = face_ids_list
all_faces = list(chain.from_iterable(df['face_encoding']))
id_face_dict = dict(enumerate(all_faces))

G = nx.Graph()
G.add_nodes_from(range(total_num_faces))
# print(df)

fe = df['face_encoding']
img_names = df['img_names']
for row_i, id_list_i in enumerate(face_ids_list):
    for row_j, id_list_j in enumerate(face_ids_list):
        if row_i >= row_j:
            continue
        for face_index in id_list_i:
            # compare each face of the current i row, with other pics. compare_faces([j_pic_faces],a_face_in_i_row)
            matches = face_recognition.compare_faces(fe[row_j], id_face_dict[face_index], tolerance=0.2)
            # print(img_names[row_j], face_index)
            # print(matches)
            if sum(matches):
                # index of faces in row_j that match current face (face_index)
                indices = [i for i, x in enumerate(matches) if x]
                # add an edge between face_indices in row_j and face_index
                for ind in indices:
                    G.add_edge(face_ids_list[row_j][ind], face_index)

output_folder = '../data/weddingphoto{}_results/'.format(test)
photo_path = '../data/weddingphotos{}/'.format(test)
if os.path.exists(output_folder):
    os.system('rm -r ' + output_folder)
os.mkdir(output_folder)
linked_id_list = [c for c in sorted(nx.connected_components(G), key=len, reverse=True)]
print(linked_id_list)
for idx, person_ids in enumerate(linked_id_list):
    person_folder = output_folder + str(idx) + "/"
    os.mkdir(person_folder)
    # find which photo has any of the person_ids
    for p in person_ids:
        for photo_idx, face_ids in enumerate(face_ids_list):
            if p in face_ids:
                os.system('cp {s} {d}'.format(s=photo_path + img_names[photo_idx],
                                              d=person_folder + img_names[photo_idx]))
                continue


