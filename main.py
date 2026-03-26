import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel
from data import table
from db_manager import get_connection
from order_dialog import OrderDialog
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Management System")

        self.tables = table
        
        widget = QWidget()
        self.setCentralWidget(widget)
        
        self.layout = QGridLayout()
        widget.setLayout(self.layout)

        self.buttons = {}

        self.create_tables()
        self.lblProfit = QLabel("Total Profit: $0.00")
        self.layout.addWidget(self.lblProfit, 3, 0, 1, 5)
    def create_tables(self):
        for i in range(1, 11):
            btn = QPushButton(f"Table {i}")
            btn.clicked.connect(lambda _, x=i: self.open_table(x))

            self.layout.addWidget(btn, (i-1)//5, (i-1)%5)
            self.buttons[i] = btn

            self.update_color(i)
    def update_color(self, table_id):
        status = self.tables[table_id]["status"]
        btn = self.buttons[table_id]
        if status == "empty":
            btn.setStyleSheet("background-color: green")
        elif status == "reserved":
            btn.setStyleSheet("background-color: yellow")
        else:
            btn.setStyleSheet("background-color: red")
    def open_table(self, table_id):
        dialog = OrderDialog(table_id, self.tables)
        if self.tables[table_id]["status"] == "empty":
            self.tables[table_id]["status"] = "occupied"
        dialog = OrderDialog(table_id, self.tables)
        dialog.exec_()
        self.update_color(table_id)
        result = dialog.exec_()
        self.refresh_everything(table_id)
    def refresh_everything(self, table_id):
        self.update_color(table_id)
        self.update_profit_display()
        print(f"Đã cập nhật trạng thái bàn {table_id} và doanh thu mới.")
    def show_total_profit(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select sum(total_amount), sum(profit) from orders")
        res = cur.fetchone()
        revenue = res[0] if res[0] else 0
        profit = res[1] if res[1] else 0
        self.statusBar().showMessage(f"Tổng doanh thu: ${revenue:.2f} | Tổng lợi nhuận: ${profit:.2f}")
        conn.close()
    def update_profit_display(self):
        from db_manager import get_total_profit
        revenue, profit = get_total_profit()
        self.lblProfit.setText(f"Total Profit: ${profit:.2f} | Total Revenue: ${revenue:.2f}")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("select sum(profit) from orders where order_time::date = current_date")
        res = cur.fetchone()
        profit = res[0] if res[0] else 0
        self.lblProfit.setText(f"Total Profit: ${profit:.2f}")
        conn.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
