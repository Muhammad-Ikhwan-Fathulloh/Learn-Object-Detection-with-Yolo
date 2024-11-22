# Learn Object Detection with YOLO

Pelajari cara menggunakan YOLO untuk deteksi objek, termasuk langkah-langkah untuk mendapatkan dataset, melatih model, menguji model, dan mengintegrasikan hasilnya dengan protokol MQTT.

---

## 📂 **Dataset**
Dataset digunakan untuk melatih model YOLO dalam mendeteksi objek tertentu (dalam contoh ini, deteksi penggunaan masker).

- **API Key**: [Dokumentasi Roboflow API](https://docs.roboflow.com/api-reference/authentication)
- **Dataset Link**: [Mask-Wearing Dataset on Roboflow](https://universe.roboflow.com/compvis-final-project/mask-wearing-9wlzj)

---

## 🛠️ **Get Dataset and Train the Model**
Langkah-langkah untuk mendapatkan dataset dan melatih model YOLO.

### 1. **Mengunduh Dataset**
Gunakan API Roboflow untuk mengunduh dataset secara otomatis dan mengkonfigurasi file `data.yaml`. Pastikan API Key Anda diatur untuk mengakses dataset.

### 2. **Melatih Model**
Gunakan skrip Python untuk melatih model YOLO. Model yang dilatih akan mendeteksi objek sesuai dengan kelas pada dataset. 

- **Source Code**: [Train YOLO Model](https://github.com/Muhammad-Ikhwan-Fathulloh/Learn-Object-Detection-with-Yolo/blob/main/Roboflow_Model_Yolo_Mask.ipynb)

---

## ✅ **Test the Model**
Setelah model selesai dilatih, Anda dapat mengujinya pada dataset validasi atau gambar/video lainnya.

- **Jalankan server**:

    Jalankan perintah berikut untuk memulai aplikasi FastAPI pada `http://127.0.0.1:8000`:

    ```bash
    uvicorn app:app --reload
    ```

    Atau, jika Anda menggunakan titik masuk (entry point) lain untuk aplikasi FastAPI:

    ```bash
    uvicorn main:app --reload
    ```

    Server akan otomatis memuat ulang setiap kali terjadi perubahan pada kode.

- **Source Code**: [Test YOLO Model](https://github.com/Muhammad-Ikhwan-Fathulloh/Learn-Object-Detection-with-Yolo/blob/main/Test_Model_Yolo_Mask.ipynb)

---

## 📡 **Integrasi MQTT**
Hasil dari deteksi objek dapat dikirim ke broker MQTT untuk diproses lebih lanjut.

### **MQTT Broker Configuration**
- **Broker URL**: `public.cloud.shiftr.io`
- **Port**: `1883`
- **Username**: `public`
- **Password**: `public`

### **MQTT Topics**
- **Input Topic**: `stream-ingestion`  
  Digunakan untuk mengirim gambar yang akan diproses.
- **Output Topic**: `ai-result`  
  Digunakan untuk menerima hasil deteksi dari AI.

---

## 🌐 **Access MQTT Client**
Untuk memonitor data yang dikirim dan diterima melalui MQTT, Anda dapat menggunakan klien MQTT berbasis web.

- **Client URL**: [HiveMQ WebSocket Client](https://www.hivemq.com/demos/websocket-client/)

---

## 📜 **Cara Kerja**
1. Unduh dataset dari Roboflow menggunakan API.
2. Latih model YOLO menggunakan dataset tersebut.
3. Uji model pada data validasi untuk memastikan kinerja model.
4. Kirim hasil deteksi melalui MQTT ke broker untuk integrasi dengan sistem lain.
5. Gunakan klien MQTT untuk memantau data secara real-time.

--- 

> **Catatan**: Pastikan Anda menggunakan GPU untuk melatih model YOLO agar proses berjalan lebih cepat. Periksa ketersediaan GPU dengan perintah `!nvidia-smi` di Google Colab.