import re

class DataProcessor:
    @staticmethod
    def clean_data(df):
        try:
            # Limpieza: eliminar caracteres especiales y espacios en blanco
            for column in df.select_dtypes(include=['object']):
                df[column] = df[column].apply(lambda x: re.sub(r'[\s\-\_.?^`[\],´]+', '', str(x)).strip())
            
            # Limpieza eliminar filas duplicadas
            df.drop_duplicates(inplace=True)
            
            return df
        
        except Exception as e:
            raise RuntimeError(f"Error al limpiar los datos del archivo Excel: {e}")

    @staticmethod
    def remove_columns(df, columns_to_keep):
        try:
            columns_to_remove = [col for col in df.columns if col not in columns_to_keep]
            df.drop(columns=columns_to_remove, inplace=True)
            return df
        except Exception as e:
            raise RuntimeError(f"Error al eliminar columnas: {e}")


