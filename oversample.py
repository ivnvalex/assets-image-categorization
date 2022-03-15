import os
import shutil


def oversample(data_path):
    """
    Oversamples minor classes in data_dir to match the largest class
    :param data_path: str, should contain subdirs with classes
    :return: None
    """
    max_images = 0
    for class_ in os.listdir(data_path):
        if class_.startswith('.'):
            continue
        max_images = max(max_images, len(os.listdir(os.path.join(data_path, class_))))
    for class_ in os.listdir(data_path):
        if class_.startswith('.'):
            continue
        class_path = os.path.join(data_path, class_)
        images = os.listdir(class_path)
        images_to_add = max_images - len(images)
        i = 0
        flag = False
        while True:
            for image in images:
                if i >= images_to_add:
                    flag = True
                    break
                split = image.split('.')
                image_name, image_format = split[0], split[1]
                copy_name = '.'.join([''.join([str(i), image_name]), image_format])
                shutil.copy2(
                    os.path.join(class_path, image),
                    os.path.join(class_path, copy_name)
                )
                i += 1
            if flag:
                break


if __name__ == '__main__':
    oversample(os.path.join(os.getcwd(), 'initial_bundle'))
