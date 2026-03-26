menu = [
    {"name": "Pizza", "price": 10.99, "image": "/assets/img/pizza.jpg"},
    {"name": "Burger", "price": 8.99, "image": "/assets/img/burger.jpg"},
    {"name": "Pasta", "price": 12.99, "image": "/assets/img/pasta.jpg"},
]
table = {
    i: {"status": "empty", "order": []} for i in range(1, 11)
}
daily_revenue = []
monthly_revenue = []