import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications.resnet_v2 import ResNet152V2
from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

from params import *


def save_model_history_plot(trained):
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    ax[0].set_title('loss')
    ax[0].plot(trained.epoch, trained.history['loss'], label='Train loss')
    ax[0].plot(trained.epoch, trained.history['val_loss'], label='Validation loss')
    ax[1].set_title('acc')
    ax[1].plot(trained.epoch, trained.history['accuracy'], label='Train acc')
    ax[1].plot(trained.epoch, trained.history['val_accuracy'], label='Validation acc')
    ax[0].legend()
    ax[1].legend()
    fig.savefig(model_history_plot_path, bbox_inches='tight')
    plt.close(fig)


datagen = ImageDataGenerator(
    horizontal_flip=True,
    preprocessing_function=preprocess_input,
    validation_split=val_size
)

print('Creating train images generator...')
train_generator = datagen.flow_from_directory(
    initial_bundle_path,
    target_size=(img_width, img_height),
    class_mode='categorical',
    batch_size=batch_size,
    subset='training'
)

print('Creating validation images generator...')
val_generator = datagen.flow_from_directory(
    initial_bundle_path,
    target_size=(img_width, img_height),
    class_mode='categorical',
    batch_size=batch_size,
    subset='validation'
)

base_model = ResNet152V2(
    include_top=False,
    weights='imagenet',
    input_shape=img_shape
)
base_model.trainable = False

model = Sequential([
    base_model,
    AveragePooling2D(pool_size=(7, 7)),
    Flatten(),
    Dense(256, activation='relu'),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(len(labels), activation='softmax')
])

optimizer = Adam(learning_rate=learning_rate)
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()

earlystopper = EarlyStopping(patience=5, verbose=1, restore_best_weights=True)
checkpointer = ModelCheckpoint(model_path, verbose=1, save_best_only=True)
print('Training the model...')
model_history = model.fit(
    train_generator,
    epochs=epochs,
    callbacks=[earlystopper, checkpointer],
    validation_data=val_generator,
    steps_per_epoch=train_images_n // batch_size,
    validation_steps=val_images_n // batch_size
)

save_model_history_plot(model_history)

test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
print('Creating test images generator...')
test_generator = test_datagen.flow_from_directory(
    test_bundle_path,
    target_size=(img_width, img_height),
    class_mode='categorical',
    batch_size=1,
    shuffle=False
)
print('Evaluating on test images...')
scores = model.evaluate(test_generator)
print(f'Test accuracy = {scores[1]*100:.4f}%')
