# GAN-Art

**🎨 GAN-Art** is a Python package designed to assist users in applying artistic style transfers to images using a GAN-based model. It provides a simple interface to transfer the artistic style of one image onto another using deep learning 🧠, specifically leveraging pre-trained TensorFlow models 🤖.

## Introduction

The **GAN-Art** package allows users to generate artistic images by blending the style of one image (such as a famous painting) onto another (such as a photograph). This is done using a pre-trained GAN model from TensorFlow Hub, which is fine-tuned through training to adapt the content and style images.

The package is simple to use and requires minimal setup. By providing paths to a content image and a style image, users can stylize images, visualize the training process, and save the final stylized image.

## Directory Structure

Assuming a standard installable Python package structure, your project directory should look like this:

```plaintext
gan-art/
│
├── gan_art/
│   ├── __init__.py          # Package Initialization
│   └── gan_art.py           # Main functionality (GANArt class)
│
├── tests/                   # Optional test cases
│   └── TODO.py      # Upcoming
│
├── README.md                # Project documentation (this file)
├── pyproject.toml           # Project dependencies and metadata
├── poetry.lock              # Poetry lock file with dependencies versions
├── LICENSE                  # License file (optional)
└── setup.py                 # Setup file for installation (optional)
```

## User Manual

### Installation

You can install the `gan-art` package using `Poetry`, or you can build and install the package locally using the following commands:

```bash
pip install gan-art
```

We simplified the dependencies of the package because we build the package for end users to solely use on Colab environment. For custom environment, one would need to install the following dependencies.

### Dependencies

The project requires the following dependencies:
- TensorFlow
- TensorFlow Hub
- NumPy
- Matplotlib
- Pillow (PIL)
- IPython (optional for notebook functionality)

These will be automatically installed if you're using `Poetry`.

### Basic Usage

Once the package is installed, you can use the `GANArt` class to apply artistic style transfer. Here's an example code snippet:

```python
from gan_art.GANArt import *

# Initialize paths to your images
content_path = 'path_to_content_image.jpg'
style_path = 'path_to_style_image.jpg'

# Create an instance of the GANArt class
gan_art = GANArt(content_path, style_path)

# Plot initial content and style images
gan_art.plot_images()

# Train the model
output_image = gan_art.train_model(epochs=10, steps_per_epoch=100)

# Save the final stylized image
tensor_to_image(output_image).save('final_stylized_image.png')
```

#### Explanation:

1. **Initialization**: The `GANArt` class is initialized with the paths to your content and style images.
2. **Plot Images**: The `plot_images` method allows you to visualize both the content and style images before training.
3. **Training**: The `train_model` method trains the GAN model using the provided images for the specified number of epochs and steps per epoch. This generates the stylized image.
4. **Saving the Image**: Finally, you can save the resulting stylized image using the `tensor_to_image()` function.

### Advanced Options

- **Epochs and Steps**: You can modify the number of epochs and steps per epoch to control how long the model trains.
- **Stylization Visualization**: During training, the image is periodically updated and displayed using Matplotlib to show the progress of the style transfer.

### Customization

The GAN model uses a pre-trained VGG-19 model for style transfer, which can be further fine-tuned or extended for other types of artistic image generation tasks. The `GANArt` class is modular, allowing you to modify components like the style and content layers, style and content weights, and training parameters.

## Author

- **Elijah Yuan**: [elijah.yuan6009@gmail.com](mailto:elijah.yuan6009@gmail.com)
- **Instructor**: **Yiqiao Yin**: [eagle0504@gmail.com](mailto:eagle0504@gmail.com)