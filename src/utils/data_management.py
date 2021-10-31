import tensorflow as tf
import logging


def train_valid_generator(data_dir, IMAGE_SIZE, BATCH_SIZE, do_data_augmentation):
    
    datagenerator_kwargs = dict(
        rescale = 1./255,
        validation_split=0.20
    )

    dataflow_kwargs = dict(
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            interpolation="bilinear"
        )
    valid_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)
    valid_generator = valid_data_generator.flow_from_directory(
        directory = data_dir,
        subset="validation",
        shuffle=False,
        **dataflow_kwargs
    )
    if do_data_augmentation:
        train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=45,
            horizontal_flip=True,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2, **datagenerator_kwargs
        )
        logging.info(f"Data augmentation is used for training")
    else:
        train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)
        logging.info(f"Data augmentation is not used for training")

    train_generator = train_data_generator.flow_from_directory(
        directory = data_dir,
        subset="training",
        shuffle=True,
        **dataflow_kwargs
    ) 
    
    logging.info(f"train & valid generator is created.")
    return train_generator, valid_generator