import MySQLdb as mdb
import atelier_sql as sql
from datetime import datetime

class AtelierDB:
    """Module which provides Atelier DB access.

    It contains knowledge of the DB schema and maps higher level
    domain models into DB structures that match the DB schema.
    """

    def __init__(self, db_host, db_user, db_password, db, logger):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db = db
        self.logger = logger

    def get_db_connection(self):
        con = mdb.connect(self.db_host, self.db_user, self.db_password, self.db)
        con.set_character_set('utf8')
        return con

    def execute_return_list(self, query, query_values):
        self.logger.debug("execute_return_list: " + query + "\n" + str(query_values))

        con = self.get_db_connection()
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute(query, query_values)
            return cur.fetchall()

    def execute_return_one(self, query, query_values):
        self.logger.debug("execute_return_one: " + query + "\n" + str(query_values))
        con = self.get_db_connection()
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute(query, query_values)
            return cur.fetchone()

    def delete(self, table, id):
        con = self.get_db_connection()
        with con:
            cur = con.cursor()
            cur.execute("delete from %s where id = %s" %(table, id))

    ## Returns the ID from the DB cursor
    def insert(self, query, query_values):
        con = self.get_db_connection()
        with con:
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute(query, query_values)
            return cur.lastrowid

    ## Post place
    def get_post_place_list(self):
        return self.execute_return_list("select * from post_place", None)

    ## Customer
    def customer(self, id):
        return self.execute_return_one("select * from customer where id = %s", (id))

    def customer_order_list(self, customer_id):
        return self.execute_return_list("select * from customer_order where customer_id = %s", (customer_id))

    def find_customers_by_name(self, name):
        # TODO find_customers_by_name : make wildcards work with prepared statement
        query = "select * from customer where first_name like %s or last_name like %s"
        return self.execute_return_list(query, (name, name))

    def update_customer(self, request_form):
        update_sql, values = sql.get_sql_and_values("customer", request_form)
        self.logger.debug(update_sql + "\n" + str(values))
        self.execute_return_one(update_sql, tuple(values))

    def set_creation_date_to_now(self, form):
        form["creation_date"] = datetime.now()

    ## Order
    def order(self, id):
        return self.execute_return_one("select * from customer_order where id = %s",
                                       (id))

    def create_order(self, request_form):
        self.set_creation_date_to_now(request_form)

        update_sql, values = sql.get_sql_and_values("customer_order",
                                                    request_form)
        self.logger.debug("update_sql="+ update_sql + "\n" + str(values))
        return self.insert(update_sql, tuple(values))

    def update_order(self, form):
        update_sql, values = sql.get_sql_and_values("order", form)
        self.logger.debug(update_sql + "\n" + str(values))
        self.execute_return_one(update_sql, tuple(values))

    def order_item(self, id):
        return self.execute_return_one("select * from order_item where id = %s",
                                       (id))

    def get_product_price(self, id):
        price = self.execute_return_one("select price from product where id = %s", (id))
        return price["price"]

    def delete_order_item(self, id):
        # TODO fix delete_order_item
        return self.delete("order_item", id)

    def order_item_list(self, order_id):
        return self.execute_return_list("select o.id, o.number_of_items, o.total_amount, o.creation_date, p.name as product_name, p.price as product_price from order_item o, product p where o.order_id = %s and o.product_id = p.id",
                                        (order_id))

    def add_order_item(self, form):
        price = self.get_product_price(form["product_id"])
        form["total_amount"] =  price *  int(form["number_of_items"])

        update_sql, values = sql.get_sql_and_values("order_item", form)
        self.set_creation_date_to_now(form)
        self.logger.debug("update_sql="+ update_sql + "\n" + str(values))
        return self.insert(update_sql, tuple(values))

    ## Product
    def product(self, id):
        return self.execute_return_one("select * from product where id = %s",
                                       (id))

    def get_product_list(self):
        return self.execute_return_list("select p.id, p.name, p.creation_date, p.production_time, p.price, pt.name from product p, product_type pt where p.product_type_id = pt.id", None)



