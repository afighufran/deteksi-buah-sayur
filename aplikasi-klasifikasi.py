import streamlit as st
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

model = load_model('FV.h5')
labels = {0: 'apel', 1: 'pisang', 2: 'bit merah', 3: 'bell pepper', 4: 'kubis', 5: 'kapsikum', 6: 'wortel',
          7: 'kembang kol', 8: 'cabe', 9: 'jagung', 10: 'timun', 11: 'terong', 12: 'bawang putih', 13: 'jahe',
          14: 'anggur', 15: 'jalapeno', 16: 'kiwi', 17: 'lemon', 18: 'selada',
          19: 'mangga', 20: 'bawang bombay', 21: 'jeruk', 22: 'paprika', 23: 'pir', 24: 'kacang polong', 25: 'nanas',
          26: 'delima', 27: 'kentang', 28: 'lobak', 29: 'kacang kedelai', 30: 'bayam', 31: 'jagung manis',
          32: 'ubi jalar', 33: 'tomat', 34: 'lobak cina', 35: 'semangka'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']


def fetch_kalori(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Tidak dapat fetch hasil kalori")
        print(e)


def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()


def run():
    st.title("Klasifikasi Buah dan Sayuran Beserta Kalori")
    img_file = st.file_uploader("Pilih Gambar", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        save_image_path = './upload_images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = processed_img(save_image_path)
            print(result)
            if result in vegetables:
                st.info('**Kategori : Sayur**')
            else:
                st.info('**Kategori : Buah**')
            st.success("**Hasil Prediksi : " + result + '**')
            cal = fetch_kalori(result)
            if cal:
                st.warning('**' + cal + '(per 100 gram)**')


run()
