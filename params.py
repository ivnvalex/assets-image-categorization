import os


labels = ('Cars', 'Plants', 'Stuff')

# paths
base_path = os.getcwd()
initial_bundle_path = os.path.join(base_path, 'initial_bundle')
test_bundle_path = os.path.join(base_path, 'test_bundle')
model_path = os.path.join(base_path, 'model.h5')
model_history_plot_path = os.path.join(base_path, 'model_history.png')

# data split parameters
val_size = 0.2
initial_images_n = 0
for class_ in os.listdir(initial_bundle_path):
    if class_.startswith('.'):
        continue
    initial_images_n += len(os.listdir(os.path.join(initial_bundle_path, class_)))
val_images_n = int(initial_images_n * val_size)
train_images_n = initial_images_n - val_images_n

# img parameters
img_width = 224
img_height = 224
img_channels = 3
img_shape = (img_width, img_height, img_channels)

# model hyperparameters
learning_rate = 1e-4
batch_size = 32
epochs = 30
