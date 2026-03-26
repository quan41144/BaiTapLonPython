create database restaurant_db;
create table menu(
	id serial primary key,
	name varchar(100),
	price numeric(10, 2),
	cost numeric(10, 2)
);
create table dining_tables(
	id int primary key,
	status varchar(20) default 'empty'
);
create table orders(
	id serial primary key,
	table_id int references dining_tables(id),
	total_amount numeric(10, 2),
	profit numeric(10, 2),
	order_time timestamp default current_timestamp
);
insert into dining_tables(id) select generate_series(1, 10);
insert into menu(name, price, cost) values
('pizza', 10.99, 5.00),
('burger', 8.99, 4.00),
('pasta', 12.99, 6.00);

alter table menu add column image text;
update menu set image = 'assets/img/pizza.jpg' where name = 'Pizza';
update menu set image = 'assets/img/burger.jpg' where name = 'Burger';
update menu set image = 'assets/img/pasta.jpg' where name = 'Pasta';