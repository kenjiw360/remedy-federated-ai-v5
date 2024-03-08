from PIL import Image, ImageOps
import requests
import pathlib
import os

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

print("Fetching Base Model From Server...")
url = 'https://a4b2-71-92-86-252.ngrok-free.app/base.keras'
r = requests.get(url)
open('base.keras', 'wb').write(r.content)
print("Finished Fetching!")

data_dir = pathlib.Path(input("Image Count: "))
image_size = (256, 256)
all_images = list(data_dir.glob('*/*.jpg'))

image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

categories = list(data_dir.glob('*/'))

os.mkdir('resized')
for (category_index, category) in enumerate(categories):
	os.mkdir(pathlib.Path('resized') / category.relative_to(data_dir))
	category_dir = list(category.glob('*.jpg'))
	for (image_index, image) in enumerate(category_dir):
		with Image.open(image) as img:
			print(f"Working on {image.name} in {category.name} (Image {image_index+1}/{len(category_dir)} of Category {category_index+1}/{len(categories)})")
			resized_img = ImageOps.fit(img, image_size)
			resized_img.save(pathlib.Path('resized') / image.relative_to(data_dir))
	print("Finished!")

data_dir = data_dir.parent / 'resized'

batch_size = 32
img_height = 256
img_width = 256

train_ds = tf.keras.utils.image_dataset_from_directory(
	data_dir,
	validation_split=0.2,
	subset="training",
	seed=123,
	image_size=(img_height, img_width),
	batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
	data_dir,
	validation_split=0.2,
	subset="validation",
	seed=123,
	image_size=(img_height, img_width),
	batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = len(class_names)

model = keras.saving.load_model("base.keras")

model.compile(optimizer='adam',
	loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
	metrics=['accuracy']
)

epochs=10
history = model.fit(
	train_ds,
	validation_data=val_ds,
	epochs=epochs
)

model.save('additiontest.keras')