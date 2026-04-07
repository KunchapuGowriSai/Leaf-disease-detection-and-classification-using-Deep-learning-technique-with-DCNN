# 🌿 Leaf Disease Detection and Classification using Deep Learning (DCNN)

## 📌 Project Overview
This project presents a Deep Convolutional Neural Network (DCNN) based system for detecting and classifying plant leaf diseases. The model analyzes leaf images and predicts the disease category, helping farmers and researchers take early action.

The application is deployed using Gradio on Hugging Face Spaces, allowing users to upload leaf images and get instant predictions.

---

## 🚀 Live Demo
Try the app here:  
https://huggingface.co/spaces/GowriSaiKunchapu/Leaf-disease-detection-and-classification-using-Deep-learning-technique-with-DCNN

---

## 🎯 Objectives
- Detect plant leaf diseases automatically  
- Classify multiple disease categories  
- Provide fast and accurate predictions  
- Enable real-time usage through a web interface  

---

## 🧠 Technologies Used
- Python  
- TensorFlow & Keras  
- Deep Learning (CNN & DCNN)  
- NumPy, Pandas  
- Matplotlib & Seaborn  
- Gradio  
- Hugging Face Spaces  

---

## 📂 Dataset
- Leaf images collected from:
  - Kaggle datasets  
  - Public plant disease datasets  
- Includes:
  - Healthy leaves  
  - Diseased leaves (multiple classes)  

---

## ⚙️ Model Architecture
- Deep Convolutional Neural Network (DCNN)
- Convolutional Layers  
- Max Pooling Layers  
- Dropout (to reduce overfitting)  
- Fully Connected Dense Layers  
- Activation Functions: ReLU, Softmax  
- Loss Function: Categorical Crossentropy  

---

## 🔄 Workflow
1. Image Input  
2. Image Preprocessing (Resizing, Normalization)  
3. Feature Extraction using CNN  
4. Classification  
5. Output Prediction  

---

## 📊 Results
- Achieved high accuracy in classification  
- Good generalization on test dataset  
- Works effectively on real-time uploaded images  

---

## 🖥️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/KunchapuGowriSai/Leaf-disease-detection-and-classification-using-Deep-learning-technique-with-DCNN.git

# Navigate into the project folder
cd Leaf-disease-detection-and-classification-using-Deep-learning-technique-with-DCNN

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py


📸 Usage
Open the application
Upload a leaf image
Click on Predict
View the detected disease result

Leaf-disease-detection-and-classification-using-Deep-learning-technique-with-DCNN/
│
├── app.py
├── model/
│   └── plant_model.keras
├── dataset/
├── static/
├── requirements.txt
└── README.md

🔮 Future Enhancements
Add more plant species
Improve model accuracy with larger datasets
Deploy mobile application
Add treatment recommendation system
Predict disease severity


📜 Publication

This project is published in a Springer Conference[https://link.springer.com/chapter/10.1007/978-3-032-13177-5_34].
