import pandas as pd

from processors.spoton_assignment.file_processor import FileProcessor


class OrderItemsProcessor(FileProcessor):

    def transform(self):
        df = pd.read_csv(self.filepath)
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'])
        df.to_csv(self.filepath.replace("preprocessed-files", "processed-files"), index=False)
