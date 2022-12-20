from processors.spoton_assignment.file_processor import FileProcessor
from processors.spoton_assignment.customers import CustomersProcessor
from processors.spoton_assignment.orders import OrdersProcessor
from processors.spoton_assignment.products import ProductsProcessor
from processors.spoton_assignment.order_items import OrderItemsProcessor


def get_file_processor(filepath: str) -> FileProcessor:
    filename = filepath.split("/")[-1]
    if filename == 'olist_customers_dataset.csv':
        return CustomersProcessor(filepath)
    elif filename == 'olist_orders_dataset.csv':
        return OrdersProcessor(filepath)
    elif filename == 'olist_products_dataset.csv':
        return ProductsProcessor(filepath)
    elif filename == 'olist_order_items_dataset.csv':
        return OrderItemsProcessor(filepath)
    else:
        raise Exception(f'File {filename} is not supported')
