import inflection
import pandas as pd

from processors.spoton_assignment.file_processor import FileProcessor


class ProductsProcessor(FileProcessor):

    def transform(self):
        df = pd.read_csv(self.filepath)

        cols = [
            'product_name_lenght',
            'product_description_lenght',
            'product_photos_qty',
            'product_weight_g',
            'product_length_cm',
            'product_height_cm',
            'product_width_cm'
        ]
        df[cols] = df[cols].fillna(-1)
        df = df.astype({col: int for col in cols})
        df['product_category_name'] = df['product_category_name'].map(
            lambda cc: inflection.titleize(cc) if cc == cc else cc)

        df.to_csv(self.filepath.replace("preprocessed-files", "processed-files"), index=False)
