from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QComboBox, QLabel
from data import menu
from db_manager import get_all_menu, get_connection, save_order_to_db, update_table_status
class OrderDialog(QDialog):
    def __init__(self, table_id, tables):
        super().__init__()
        self.menu_data = get_all_menu()
        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(150, 150)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.imageLabel, alignment=Qt.AlignCenter)

        self.comboFood.currentIndexChanged.connect(self.update_image)
        self.update_food_image()

        self.setWindowTitle(f"Order for Table {table_id}")
        self.table_id = table_id
        self.tables = tables

        layout = QVBoxLayout()

        self.listOrder = QListWidget()
        layout.addWidget(self.listOrder)

        self.comboFood = QComboBox()
        for food in menu:
            self.comboFood.addItem(food["name"])
        layout.addWidget(self.comboFood)

        btnAdd = QPushButton("Add to Order")
        btnAdd.clicked.connect(self.add_to_order)
        layout.addWidget(btnAdd)

        self.lblTotal = QLabel("Total: $0.00")
        layout.addWidget(self.lblTotal)

        btnPay = QPushButton("Pay")
        btnPay.clicked.connect(self.checkout)
        layout.addWidget(btnPay)

        self.setLayout(layout)
        self.load_orders()
    def update_food_image(self):
        food_name = self.comboFood.currentText()
        image_path = ""
        for food in self.menu_data:
            if food["name"] == food_name:
                image_path = food.get('image')
                break
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.imageLabel.setText("Image not found")
        else:
            self.imageLabel.setText("No Image")
    def load_orders(self):
        self.listOrder.clear()
        total = 0
        for item in self.tables[self.table_id]["order"]:
            self.listOrder.addItem(f"{item['name']} - ${item['price']:.2f}")
            total += item["price"]
        self.lblTotal.setText(f"Total: ${total:.2f}")
    def add_to_order(self):
        food_name = self.comboFood.currentText()
        for food in menu:
            if food["name"] == food_name:
                self.tables[self.table_id]["order"].append(food)
        self.load_orders()
    def checkout(self):
        if not self.tables[self.table_id]["order"]:
            return
        total_revenue = 0
        total_cost = 0
        for item in self.tables[self.table_id]["order"]:
            total_revenue += item["price"]
            total_cost += item.get("cost", 0)
        profit = total_revenue - total_cost
        
        save_order_to_db(self.table_id, total_revenue, profit)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "insert into orders (table_id, total_revenue, profit) values (%s, %s, %s)",
            (self.table_id, total_revenue, profit)
        )
        conn.commit()
        conn.close()

        update_table_status(self.table_id, "empty")
        self.tables[self.table_id] = {"status": "empty", "order": []}
        print(f"Đã thanh toán: {total_revenue:.2f}, Lợi nhuận: {profit:.2f}")
        self.accept()