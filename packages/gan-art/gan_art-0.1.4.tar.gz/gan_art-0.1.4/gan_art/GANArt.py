import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image
import time
import tensorflow_hub as hub
from typing import Dict

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'


def tensor_to_image(tensor: tf.Tensor) -> PIL.Image.Image:
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


class StyleContentModel(tf.keras.models.Model):
    def __init__(self, style_layers: list, content_layers: list):
        super(StyleContentModel, self).__init__()
        self.vgg = self.vgg_layers(style_layers + content_layers)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)
        self.vgg.trainable = False

    def vgg_layers(self, layer_names: list) -> tf.keras.Model:
        """Creates a VGG model that returns a list of intermediate output values."""
        vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
        vgg.trainable = False
        outputs = [vgg.get_layer(name).output for name in layer_names]
        model = tf.keras.Model([vgg.input], outputs)
        return model

    def call(self, inputs: tf.Tensor) -> Dict[str, Dict[str, tf.Tensor]]:
        """Expects float input in [0,1]"""
        inputs = inputs * 255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                          outputs[self.num_style_layers:])

        style_outputs = [self.gram_matrix(style_output) for style_output in style_outputs]

        content_dict = {content_name: value
                        for content_name, value
                        in zip(self.content_layers, content_outputs)}

        style_dict = {style_name: value
                      for style_name, value
                      in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 'style': style_dict}

    @staticmethod
    def gram_matrix(input_tensor: tf.Tensor) -> tf.Tensor:
        result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
        input_shape = tf.shape(input_tensor)
        num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
        return result / num_locations


class GANArt:
    def __init__(self, content_path: str, style_path: str):
        self.content_path = content_path
        self.style_path = style_path

        # Load the hub model
        self.hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

        # Load VGG model
        self.vgg = tf.keras.applications.VGG19(include_top=True, weights='imagenet')

        # Load images
        self.content_image = self.load_img(content_path)
        self.style_image = self.load_img(style_path)

        # Define style and content layers
        self.content_layers = ['block5_conv2']
        self.style_layers = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']

        # Initialize the extractor model
        self.extractor = StyleContentModel(self.style_layers, self.content_layers)

    def load_img(self, path_to_img: str) -> tf.Tensor:
        max_dim = 512
        img = tf.io.read_file(path_to_img)
        img = tf.image.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)

        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def imshow(self, image: tf.Tensor, title: str = None):
        if len(image.shape) > 3:
            image = tf.squeeze(image, axis=0)
        plt.imshow(image)
        if title:
            plt.title(title)
        plt.show()

    def plot_images(self):
        plt.subplot(1, 2, 1)
        self.imshow(self.content_image, 'Content Image')

        plt.subplot(1, 2, 2)
        self.imshow(self.style_image, 'Style Image')
        plt.show()

    def style_content_loss(self, outputs: Dict[str, Dict[str, tf.Tensor]]) -> tf.Tensor:
        style_outputs = outputs['style']
        content_outputs = outputs['content']

        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - self.style_targets[name]) ** 2)
                               for name in style_outputs.keys()])
        style_loss *= self.style_weight / len(self.style_layers)

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - self.content_targets[name]) ** 2)
                                 for name in content_outputs.keys()])
        content_loss *= self.content_weight / len(self.content_layers)
        loss = style_loss + content_loss
        return loss

    def create_style_extractor(self):
        style_outputs = self.extractor(self.style_image * 255)['style']
        for name, output in zip(self.style_layers, style_outputs):
            print(name)
            print("  shape: ", output.shape)
            print("  min: ", output.numpy().min())
            print("  max: ", output.numpy().max())
            print("  mean: ", output.numpy().mean())

    def high_pass_x_y(self, image: tf.Tensor) -> tf.Tensor:
        x_var = image[:, :, 1:, :] - image[:, :, :-1, :]
        y_var = image[:, 1:, :, :] - image[:, :-1, :, :]
        return x_var, y_var

    def total_variation_loss(self, image: tf.Tensor) -> tf.Tensor:
        x_deltas, y_deltas = self.high_pass_x_y(image)
        return tf.reduce_sum(tf.abs(x_deltas)) + tf.reduce_sum(tf.abs(y_deltas))

    @tf.function
    def train_step(self, image: tf.Variable):
        with tf.GradientTape() as tape:
            outputs = self.extractor(image)
            loss = self.style_content_loss(outputs)
            loss += self.total_variation_weight * tf.image.total_variation(image)

        grad = tape.gradient(loss, image)
        self.opt.apply_gradients([(grad, image)])
        image.assign(self.clip_0_1(image))

    def train_model(self, epochs: int = 10, steps_per_epoch: int = 100):
        image = tf.Variable(self.content_image)
        self.opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

        # Set style/content targets
        self.style_targets = self.extractor(self.style_image)['style']
        self.content_targets = self.extractor(self.content_image)['content']

        self.style_weight = 1e-2
        self.content_weight = 1e4
        self.total_variation_weight = 30

        start = time.time()

        step = 0
        for n in range(epochs):
            for m in range(steps_per_epoch):
                step += 1
                self.train_step(image)
                print(".", end='', flush=True)
            plt.figure(figsize=(12, 12))
            plt.imshow(tensor_to_image(image))
            plt.title(f"Train step: {step}")
            plt.show()

        end = time.time()
        print(f"Total time: {end - start:.1f} seconds")
        return image

    @staticmethod
    def clip_0_1(image: tf.Tensor) -> tf.Tensor:
        return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)
