from flask import Flask, request, jsonify, render_template
from data_processor import DataProcessor
import pandas as pd
from io import BytesIO
import xlsxwriter
import numpy as np

app = Flask(__name__)

# Lista de columnas que deseas mantener
columns_to_keep = ['placa_vehiculo']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se proporcionó ningún archivo'})

    if file:
        try:
            # Leer el archivo Excel
            df = pd.read_excel(BytesIO(file.read()))
            # Limpiar los datos
            cleaned_df = DataProcessor.clean_data(df)
    
            # Remover las columnas que no deseas mantener
            cleaned_df = DataProcessor.remove_columns(cleaned_df, columns_to_keep)
    
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output, {'nan_inf_to_errors': True})
            worksheet = workbook.add_worksheet()
            
            # Escribir los datos limpios en el libro de Excel
            for i, row in cleaned_df.iterrows():
                for j, value in enumerate(row):
                    if isinstance(value, pd.Timestamp):
                        # Convertir el Timestamp a Unix timestamp
                        float_value = value.timestamp()
                    else:
                         try:
                             float_value = float(value)
                         except ValueError:
                             float_value = value

 
                        
                    if pd.isna(float_value) or (isinstance(float_value, float) and np.isinf(float_value)):
                        worksheet.write_string(i, j, '', workbook.add_format({'font_color': 'red'}))
                    else:
                        worksheet.write(i, j, float_value)
            
            workbook.close()
            
            output.seek(0)
            return jsonify({'success': True, 'file': output.read().decode('latin1')})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'No se pudo procesar el archivo'})
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
