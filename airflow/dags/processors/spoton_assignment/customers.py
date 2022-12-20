import inflection
import pandas as pd

from processors.spoton_assignment.file_processor import FileProcessor


class CustomersProcessor(FileProcessor):

    def transform(self):
        df = pd.read_csv(self.filepath)
        df['customer_city'] = df['customer_city'].map(lambda cc: inflection.titleize(cc))
        df['customer_state'] = df['customer_state'].map(lambda cc: cc.upper())
        df.to_csv(self.filepath.replace("preprocessed-files", "processed-files"), index=False)
