import csv

# Path to your CSV file
csv_file_path = 'skuStock.csv'

with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.reader(file)
    
    headers = next(reader)

    sql_statements = []

    for row in reader:
        sku = row[0]
        try:
            qty = int(float(row[1].replace(',', '.')))
        except ValueError:
            qty = 0
        
        if qty < 0:
            qty = 0
        
        is_in_stock = 1 if qty > 0 else 0
        
        sql_statement = f"""
        UPDATE cataloginventory_stock_item AS csi
        JOIN catalog_product_entity AS cpe ON csi.product_id = cpe.entity_id
        SET csi.qty = {qty}, csi.is_in_stock = {is_in_stock}
        WHERE cpe.sku = '{sku}';
        """
        sql_statements.append(sql_statement)

output_sql_file_path = 'output_sql_statements.sql'
with open(output_sql_file_path, mode='w') as sql_file:
    sql_file.writelines(sql_statements)

print(f"SQL statements have been generated")
