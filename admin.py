import tkinter as tk
from tkinter import ttk

class OnlineShoppingAdminGUI:
    def __init__(self, root,connection,cursor):
        self.root = root
        self.root.title("Online Shopping Admin Panel")

        # MySQL Connection
        self.db = connection
        self.cursor = cursor

        # Fetch available tables
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]

        # Table selection
        self.table_label = tk.Label(root, text="Select Table:")
        self.table_label.pack()
        self.table_var = tk.StringVar()
        self.table_combobox = ttk.Combobox(root, textvariable=self.table_var, values=tables)
        self.table_combobox.pack()

        # Column selection
        self.column_label = tk.Label(root, text="Select Column:")
        self.column_label.pack()
        self.column_var = tk.StringVar()
        self.column_combobox = ttk.Combobox(root, textvariable=self.column_var, state="disabled")
        self.column_combobox.pack()

        # Action selection
        self.action_label = tk.Label(root, text="Select Action:")
        self.action_label.pack()
        self.action_var = tk.StringVar()
        self.action_combobox = ttk.Combobox(root, textvariable=self.action_var, values=["Read", "Update", "Delete", "Nested Query", "Join Query", "Aggregate Query"])
        self.action_combobox.pack()

        # Entry for new value
        self.new_value_label = tk.Label(root, text="New Value:")
        self.new_value_label.pack()
        self.new_value_var = tk.StringVar()
        self.new_value_entry = tk.Entry(root, textvariable=self.new_value_var)
        self.new_value_entry.pack()

        # Entry for user ID
        self.user_id_label = tk.Label(root, text="User ID:")
        self.user_id_label.pack()
        self.user_id_var = tk.StringVar()
        self.user_id_entry = tk.Entry(root, textvariable=self.user_id_var)
        self.user_id_entry.pack()

        # Treeview for displaying results
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ()
        self.tree.heading("#0", text="Results")
        self.tree.pack()

        # Execute button
        self.execute_button = tk.Button(root, text="Execute", command=self.execute_action)
        self.execute_button.pack()

        # Buttons for specific queries
        self.nested_query_button = tk.Button(root, text="Nested Query", command=self.execute_nested_query)
        self.nested_query_button.pack()

        self.join_query_button = tk.Button(root, text="Join Query", command=self.execute_join_query)
        self.join_query_button.pack()

        self.aggregate_query_button = tk.Button(root, text="Aggregate Query", command=self.execute_aggregate_query)
        self.aggregate_query_button.pack()

        # Event bindings
        self.action_var.trace_add("write", self.enable_disable_column_selection)
        self.table_var.trace_add("write", self.populate_columns)

    def enable_disable_column_selection(self, *args):
        action = self.action_var.get()
        if action in ["Update", "Delete"]:
            self.column_combobox.config(state="readonly")
        else:
            self.column_combobox.set("")
            self.column_combobox.config(state="disabled")

    def populate_columns(self, *args):
        table = self.table_var.get()
        if table:
            self.cursor.execute(f"SHOW COLUMNS FROM {table}")
            columns = [column[0] for column in self.cursor.fetchall()]
            self.column_combobox["values"] = columns
        else:
            self.column_combobox.set("")
            self.column_combobox["values"] = []

    def execute_action(self):
        table = self.table_var.get()
        column = self.column_var.get()
        action = self.action_var.get()

        if action == "Read":
            query = f"SELECT * FROM {table}"
            self.display_results(query)
        elif action == "Update":
            new_value = self.new_value_var.get()
            user_id = self.user_id_var.get()

            if column and new_value and user_id:
                # Use proper escaping to prevent SQL injection
                new_value = self.db.escape_string(new_value)
                user_id = self.db.escape_string(user_id)

                query = f"UPDATE {table} SET {column} = '{new_value}' WHERE user_id = '{user_id}'"
                self.execute_query(query)
            else:
                print("Please provide values for column, new value, and user ID.")
        elif action == "Delete":
            user_id = self.user_id_var.get()
            query = f"DELETE FROM {table} WHERE user_id = '{user_id}'"
            self.execute_query(query)
        # Add more conditions for other actions if needed

    def execute_nested_query(self):
        query = "SELECT * FROM users WHERE User_ID IN (SELECT User_ID FROM orders)"
        self.display_results(query)

    def execute_join_query(self):
        query = "SELECT cart_items.itemname, cart_items.price, cart_items.Size, products.itemcode, products.Price, products.Category_ID, products.Product_Description FROM cart_items INNER JOIN products ON cart_items.itemname = products.itemname"
        self.display_results(query)

    def execute_aggregate_query(self):
        query = "SELECT SUM(products.Price) AS TotalPrice FROM cart_items INNER JOIN products ON cart_items.itemname = products.itemname"
        self.display_results(query)

    def execute_query(self, query):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute(query)
            self.db.commit()
            print("Operation successful.")
        except Exception as e:
            print(f"Error: {e}")
            self.db.rollback()

    def display_results(self, query):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            self.tree["columns"] = tuple(columns)
            self.tree.heading("#0", text="Results")
            for col in columns:
                self.tree.heading(col, text=col)
            for row in self.cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineShoppingAdminGUI(root,connection,cursor)
    root.mainloop()
