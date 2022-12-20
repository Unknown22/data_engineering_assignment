import pandas as pd

from processors.spoton_assignment.file_processor import FileProcessor


class OrdersProcessor(FileProcessor):

    def transform(self):
        df = pd.read_csv(self.filepath)
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])
        df['order_delivered_carrier_date'] = pd.to_datetime(df['order_delivered_carrier_date'])
        df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
        df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
        df.to_csv(self.filepath.replace("preprocessed-files", "processed-files"), index=False)
