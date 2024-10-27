def openai_read_configuration(video_file):
    with open(video_file, 'r') as file:
        contenuto = file.read()
    return contenuto