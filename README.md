# photo_face_split

Group photos by the faces in it.

Uses face_recognition package and dlip is required. Installation guide for dlip https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf.

Convert all photos in album and save into pickle file.

Run ```python pre_processing.py```

Do pairwise comparisons of faces across photos and construct a network with
nodes as faces, and edges if two faces are similar. Each isolated subgraphs
will be taken as a person and images with the person is written to a separate
folder.

Run ```python run.py```

