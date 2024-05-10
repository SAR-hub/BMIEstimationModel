from pathlib import Path
import cv2
import numpy as np
import tensorflow.keras as keras
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")
# Load the uploaded image
uploaded_files = Path("temp_images").glob("*")
input_filename = next(iter(uploaded_files)).stem
raw_input_image = cv2.imread("temp_images/" + input_filename + ".jpg")
raw_input_image = cv2.cvtColor(raw_input_image, cv2.COLOR_BGR2RGB)

# Resize the input image to (2048, 2048)
resized_input_image = cv2.resize(raw_input_image, (2048, 2048))

# Preprocess the input image
preprocessed_input_image = resized_input_image / 255.0  # Normalize pixel values
preprocessed_input_image = np.expand_dims(preprocessed_input_image, axis=0)  # Add batch dimension

# Load the model without compiling
model = keras.models.load_model('3.935_model.h5', compile=False)

# Reshape the input image to match the expected shape
preprocessed_input_image = np.reshape(preprocessed_input_image, (-1, 2048))

# Predict BMI
preds = model.predict(preprocessed_input_image)
bmi_pred = preds[0][0]
print(f"BMI: {bmi_pred}")


