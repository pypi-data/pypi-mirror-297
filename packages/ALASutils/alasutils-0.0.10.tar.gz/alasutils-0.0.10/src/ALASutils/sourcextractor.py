from subprocess import PIPE, Popen
import subprocess as sp

class SourceXtractor:
    def __init__(self, config_file=None, zeropoint_file=None):
        """
        Inicializa la clase SourceXtractor con un archivo de configuración opcional.
        :param config_file: Ruta al archivo de configuración de SourceXtractor++
        """
        self.config_file = config_file
        self.zeropoint_file = zeropoint_file  # Agregamos el archivo de datos de punto de cero
        self.params = {}
        self.zeropoints_df = self._load_zeropoints() if zeropoint_file else None
        
    def _load_zeropoints(self):
        """
        Carga los puntos de cero desde el archivo especificado en formato pandas DataFrame.
        :return: DataFrame con los puntos de cero (filtros como columnas, nombre de campo como índice).
        """
        # Suponiendo que el archivo está en formato CSV con el nombre del campo como índice
        zeropoints_df = pd.read_csv(self.zeropoint_file, index_col=0)
        return zeropoints_df

    def get_zeropoints(self, filters, field_name):
        """
        Devuelve una lista de puntos de cero para los filtros proporcionados y un campo específico.
        :param filters: Lista de nombres de filtros.
        :param field_name: Nombre del campo (índice en el archivo de puntos de cero).
        :return: Lista de puntos de cero correspondientes a los filtros para ese campo.
        """
        if self.zeropoints_df is None:
            raise ValueError("No se ha cargado ningún archivo de puntos de cero.")

        if field_name not in self.zeropoints_df.index:
            raise ValueError(f"El campo {field_name} no se encuentra en el archivo de puntos de cero.")
            
        nbands = []
        for band in filters:
            if band in [ 'U', 'G', 'R', 'I', 'Z' ]: # Cambio la banda para que se ajuste con las de SPLUS
                band = 'ZP_' + band.lower()
            elif band in [ 'F378', 'F395', 'F410', 'F430', 'F515', 'F660', 'F861' ]:
                band = 'ZP_J0' + band[1:]
            nbands.append(band)
        
        # Extraer los puntos de cero para los filtros especificados
        zeropoints = self.zeropoints_df.loc[field_name, nbands].tolist()
        return zeropoints
    
    def set_config_file(self, config_file):
        """
        Establece un archivo de configuración.
        :param config_file: Ruta al archivo de configuración.
        """
        self.config_file = config_file

    def set_param(self, key, value):
        """
        Establece un parámetro adicional que se pasará durante la ejecución.
        :param key: Nombre del parámetro.
        :param value: Valor del parámetro.
        """
        self.params[key] = value

    def build_command(self, output_catalog):
        """
        Construye el comando que ejecuta SourceXtractor++ con los parámetros especificados.
        :param input_image: Ruta a la imagen de entrada (formato FITS).
        :param output_catalog: Ruta al archivo de catálogo de salida.
        :return: Lista con el comando completo.
        """
        command = ['sourcextractor++', '--output-catalog-filename', output_catalog]
        
        if self.config_file:
            command.extend(['--config-file', self.config_file])
        
        for key, value in self.params.items():
            if key == 'python-arg':
                # Añadir los múltiples argumentos que se pasan con 'python-arg'
                command.extend([f'--{key}' + " \'" + str(value) + "\'"])
            else:
                command.extend([f'--{key}', str(value)])
        
        return command

    def run(self, output_catalog):
        """
        Ejecuta el comando SourceXtractor++.
        :param input_image: Ruta a la imagen de entrada (FITS).
        :param output_catalog: Ruta al archivo de catálogo de salida.
        :return: Salida estándar y error estándar de la ejecución.
        """
        command = self.build_command( output_catalog)
        print(f"Ejecutando comando:\n{' '.join(command)}")
        
        try:
            # Reemplazar el uso de subprocess.run por Popen para capturar la salida sin mostrarla.
            with Popen(' '.join(command), stdout=PIPE, stderr=sp.STDOUT, shell=True) as process:
                sextractor_output = process.communicate()[0].decode("utf-8")
                #print("Ejecución exitosa")
                return sextractor_output, None
        except sp.CalledProcessError as e:
            print(f"Error durante la ejecución: {e.stderr}")
            return None, e.stderr


