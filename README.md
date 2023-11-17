# Algeo02-22135

<h2 align="center">
  🟥🟧🟨🟩🟦🟪 Simple CBIR Program 🟥🟧🟨🟩🟦🟪 <br/>
</h2>
<hr>

> Watch the Live demo [_here_](https://www.example.com).

## Table of Contents

- [Deskripsi Permasalahan](#Deksripsi-Permasalahan)
- [Anggota Kelompok](#Anggota-Kelompok)
- [Fitur](#Fitur)
- [Libraries Yang Digunakan](#Libraries-Yang-Digunakan)
- [Struktur Program](#Struktur-Program)
- [Cara Menggunakan](#Cara-Menggunakan)
- [Screenshot](#Screenshot)
- [Project Status](#project-status)
- [Acknowledgements](#acknowledgements)

## Deskripsi Permasalahan

Content-Based Image Retrieval (CBIR) merupakan proses pencarian dan pengambilan gambar berdasarkan konten visualnya. Tahapan awalnya melibatkan ekstraksi fitur-fitur utama dari gambar seperti warna, tekstur, dan bentuk. Fitur-fitur ini kemudian diubah menjadi vektor atau deskripsi numerik yang bisa dibandingkan dengan gambar lain.

Pada projek ini, akan dibuat program CBIR menggunakan parameter warna dan tekstur. Program ini akan diimplementasikan dalam website lokal yang menerima input gambar yang ingin dibandingkan beserta folder dataset yang menjadi pembanding

## Anggota Kelompok

| NIM      | Nama                       | Tanggung Jawab         |
| -------- | -------------------------- | ---------------------- |
| 13522135 | Christian Justin Hendrawan | Algoritma CBIR warna   |
| 13522143 | Muhammad Fatihul Irhab     | Algoritma CBIR tekstur |
| 13522146 | M. Zaidan sa’dun R.        | Front-End website      |

## Fitur

1. CBIR Colour
2. CBIR Tekstur

## Libraries Yang Digunakan

- OpenCV
- NumPy
- FastAPI

## Struktur Program

```
.
│
├── doc
│   └── Algeo02-21055.pdf
│
├── src
│   ├── _pycache_
│   ├── background
│   │   ├─── background.png
│   │   ├─── background2.png
│   │   └─── image_bg.png
│   │
│   ├── buttons
│   │   ├─── img0.png
│   │   ├─── img1.png
│   │   ├─── img2.png
│   │   ├─── img3.png
│   │   └─── img4.png
│   │
│   ├── icon
│   │   └─── logo.png
│   │
│   ├── textbox
│   │   ├─── img_textBox0.png
│   │   ├─── img_textBox1.png
│   │   ├─── img_textBox2.png
│   │   ├─── img_textBox3.png
│   │   └─── img_textBox4.png
│   │
│   ├── app.py
│   ├── eigen.py
│   ├── image.py
│   ├── model.py
│   ├── utilities.py
│   └── video.py
│
├── test
│   ├── _pycache_
│   ├── dataset
│   └── pencocokan.py
│
└── README.md
```

## Cara Menggunakan

1. Please make sure you've installed tkinter and all the above technologies that we use
2. In `src/` folder type `python app.py`
3. Begin to use our app, select your own dataset and your own test-image

## Screenshot

![Example screenshot](./img/screenshot.png)
Video [this tutorial](https://www.example.com).

## Project Status

Project is: _complete_

## Acknowledgements

Terima kasih sebesar-besarnya kepada :

- Tuhan YME
- Asisten lab IRK
- Dosen pengampu IF2123 Dr. Ir. Rinaldi Munir, M.T.
