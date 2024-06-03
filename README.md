
# Plant Leaf Detection API

> Plant Snap mobile app: (https://github.com/dinhvan2310/PlantSnap)

This FastAPI application provides an API for detecting plant species and health status based on leaf images. The model is trained on a custom dataset of leaf images and uses a multi-task learning approach to predict both the plant species and health status.

## Features

- Accepts image uploads and returns the detected plant species and status Health or Unhealthy.
- Utilizes a machine learning model trained on a self-collected dataset of leaf images.
- Provides a simple and intuitive API for integration with mobile applications or other systems.

## Tech Stack

- Python
- FastAPI
- TensorFlow
- NumPy
- OpenCV

## API Endpoints

### Upload Single Image
**Endpoint:** `/api/predict`

**Method:** POST

**Request Body:** `file` (binary file)

**Response:** JSON object with the detected plant species.

Example Request:
```
curl -X POST -F 'file=@leaf.jpg' http://localhost:5000/api/predict
```

Example Response:
```json
{
    "status": 0,
    "plant_id_top1": 2,
    "plant_id_top2": 1,
    "plant_id_top3": 9,
    "score_top1": 86,
    "score_top2": 12,
    "score_top3": 1
}
```

### Get All Plant Species
**Endpoint:** `/api/plants`

**Method:** GET

**Request Body:** None

**Response:** JSON object with the list of plant species.

Example Request:
```
curl -X GET http://localhost:5000/api/plants
```

Example Response:
```json
[
    {
        "id": 0,
        "name": "Cachua"
    },
    {
        "id": 1,
        "name": "Diepca"
    },
    ...
]
```

### Get Plant Species by ID
**Endpoint:** `/api/plants/<int:plant_id>`

**Method:** GET

**Request Body:** None

**Response:** JSON object with the plant species details.

Example Request:
```
curl -X GET http://localhost:5000/api/plants/1
```

Example Response:
```json
{
    "id_leaf": 0,
    "name": "Lá cà chua",
    "scientific_name": "Solanum Lycopersicum",
    "another_name": "cà dầm, tomate (Pháp)",
    "url_image": [
      "https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/Directory%2Fcachua.jpg?alt=media&token=4610126c-a468-4e6f-9ac1-ca115999fafc",
      "https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/Directory%2Fcachua1.jpg?alt=media&token=43b12095-7b9a-440d-bbca-38479f3afa31",
      "https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/Directory%2Fcachua2.jpg?alt=media&token=e931e3dd-7ee4-4c57-b85a-f7183940745a",
      "https://firebasestorage.googleapis.com/v0/b/plantsnap-419307.appspot.com/o/Directory%2Fcachua3.jpg?alt=media&token=70c8a6ed-2245-43a7-84f3-95e5fabf4e9e"
    ],
    "description": "Cây thảo, sống theo mùa. Thân tròn, phân cành nhiều. Lá có cuống dài, phiến lá xẻ lông chim, số lượng thùy không ổn định,\n thường có răng cưa. Hoa họp thành những xim thưa ở nách lá, cuống phủ lông cứng. \nĐài 3-6 thùy hình mũi mác không dài hơn đài, mặt phủ lỏng. Nhị 5-6, bao phấn dính thành 1 ống bao quanh nhụy, thuôn dần ở đỉnh, mở bằng những kẽ nứt dọc ngắn. Bầu có 3 hoặc nhiều ô, mỗi ô chứa nhiều noãn. Quả mọng có 3 ô. Hạt dẹt, hình thận. Do một quá trình trồng trọt lâu đời, nên Cây cà chua có nhiều biến đổi về hình thái, số lượng các thùy của đài, tràng, bộ nhị có khi 5, 6, 7 có khi 8. Số lượng lá noãn cũng tăng lên nhiều. Mùa hoa quả: mùa đông và mùa xuân",
    "ingredient": "Carotenoid, Vitamin C, Kali, Folate, Chất sơ, Can xi, Phốt pho, Ma giê, Ka li, Lưu huỳnh… và các vitamin như A, B1, B3, B6, C (4).",
    "uses": "cải thiện thị lực. Phòng chống ung thư. Làm sáng da. Giảm lượng đường trong máu. Thúc đẩy giấc ngủ ngon. Giữ xương chắc khoẻ. Chữa các bệnh mãn tính. Tốt cho mái tóc của bạn. Giúp giảm cân.",
    "medicine": "•\tLá cà chua có tác dụng: làm giảm kích ứng da do bị sâu bọ đốt bằng cách rửa sạch vò nát , rồi xát lên da. Ngoài ra trong y học , lá cà chua(đã phơi khô) có được dùng làm nguyên liệu chiết xuất tomatine(chất kháng khuẩn và chống nấm) . \n•\tTác dụng ngọn cà chua: làm giảm mụn nhọt và viêm tấy .\n•\tQuả cà chua có tác dụng: Bổ máu, hạ sốt, nhuận tràng và giảm táo bón, sinh tân dịch cho cơ thể, giúp điều hoà quá trình bài tiết, tốt cho mọi người bị sỏi niệu đạo, tốt cho người kém ăn, suy nhược và bị nhiễm độc mãn tính, tốt cho người bị xơ cứng động mạch. \n•\tMột số bài thuốc dùng quả và vỏ quả cà chua: Điều trị khô miệng, rát lưỡi, điều trị bỏng, điều trị sốt cao kèm theo khát nước, điều trị viêm gan mạn tính\n",
    "effect_medicine": "Gây trào ngược dạ dày, ợ chua. Chứng đau nữa đầu. Dị ứng nhiễm trùng. Gây sỏi thận. Gây hội chứng ruột kích thích. Gây đau khớp. Gây tiêu chảy,gây các vấn đề hô hấp....",
    "note_use": "Lựa chọn: Ngoài vấn đề cà chua ngâm tẩm hóa chất bảo quản, khi mua cà chua bạn cũng nên chọn nhà cung cấp uy tín để tránh mua nhầm hàng vượt quá dư lượng thuốc trừ sâu \n(cây cà chua rất dễ bị sâu phá hoại nên người trồng thường phải phun thuốc rất nhiều – tương tự như đậu bắp và đậu đũa vậy).\n•\tSơ chế: Chỉ nên ăn những quả cà chua đã chín đỏ hoàn toàn và rửa thật sạch với nước hoặc nước muối, nước vo gạo. Bên cạnh đó, không nên ăn cà chua lúc đói và không ăn cà chua đã nấu chín quá kỹ.\n•\tLiều lượng: Mỗi ngày, mỗi người bình thường chỉ nên ăn khoảng 1 quả cà chua và không nên ăn cà chua liên tục trong nhiều ngày (vì sẽ dẫn đến vàng da).\n•\tLàm đẹp: Thịt quả cà chua có thể dùng làm mặt nạ dưỡng da, tuy nhiên, những người có da nhạy cảm cần cẩn trọng vì cà chua có thể làm tình trạng da xấu hơn.\n•\tĐối tượng: Những người bị các bệnh về đường tiêu hóa cần cân nhắc khi dùng cà chua.\n"
  },
```


## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/dinhvan2310/PlantSnap_API
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Train the custom model using the provided Jupyter notebook:
```
Multi_task_learning.ipynb 
```

5. Run the Flask application:
```
python main.py
```

The server will start running on `http://localhost:5000`.

## Documentation

The API documentation is available at `http://localhost:5000/docs`.

## Contribution

If you find any issues or have suggestions for improvement, feel free to open a new issue or submit a pull request.
