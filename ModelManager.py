# Create a Manager for a Tensorflow Model that contains all data that you would need over time
# Essentially is a wrapper for models that allow access to other functionality in the models
import TimeLogger.TimeLogger as tl
import tensorflow as tf
import numpy as np
from enum import Enum

class TensorInitSetting(Enum):
    RANDOM = 'random'
    ZEROS = 'zeros'
    ONES = 'ones'

class ModelManager:

    #  tf.dtypes.as_dtype("float32") to convert string to tensorflow datatype
    def __init__(self, tensorflow_model: tf.keras.Model, input_shape: tuple, dtype: str):
        self.tf_model = tensorflow_model
        self.input_shape = input_shape
        self.dtype = dtype
        self.single_sample_input = None
        self.batch_sample_input = None
        self.time_manager = tl.TimeManager()

    def create_sample_input(self, setting: TensorInitSetting, batch_size=1):

        # Initialize Shape List
        shape_list = [self.input_shape[i] for i in len(self.input_shape)]

        # If that shape_list has a batch size of NONE then change NONE to batch_size
        if shape_list[0] == None:
            shape_list[0] = batch_size

        if setting == TensorInitSetting.RANDOM:
            temp_shape = self.input_shape
            if temp_shape[0] == None:
                temp_shape[0] = batch_size
            random_np_array = np.random.randint(10, size=self.input_shape)
            return tf.convert_to_tensor(random_np_array, dtype=tf.dtypes.as_dtype(self.dtpye))
        elif setting == TensorInitSetting.ZEROS:
            return tf.ones(shape_list, dtype=tf.dtypes.as_dtype(self.dtpye))
        elif setting == TensorInitSetting.ONES:
            return tf.zeros(shape_list, dtype=tf.dtypes.as_dtype(self.dtpye))
        else:
            raise Exception("NOT ENOUGH INFORMATION TO CREATE SAMPLE")

    def create_sample_input(self, setting: str, batch_size=1):
        # Initialize Shape List
        shape_list = [self.input_shape[i] for i in len(self.input_shape)]

        # If that shape_list has a batch size of NONE then change NONE to batch_size
        if shape_list[0] == None:
            shape_list[0] = batch_size

        if setting == 'random':
            temp_shape = self.input_shape
            if temp_shape[0] == None:
                temp_shape[0] = batch_size
            random_np_array = np.random.randint(10, size=self.input_shape)
            return tf.convert_to_tensor(random_np_array, dtype=tf.dtypes.as_dtype(self.dtpye))
        elif setting == 'zeros':
            return tf.ones(shape_list, dtype=tf.dtypes.as_dtype(self.dtpye))
        elif setting == 'ones':
            return tf.zeros(shape_list, dtype=tf.dtypes.as_dtype(self.dtpye))
        else:
            raise Exception("NOT ENOUGH INFORMATION TO CREATE SAMPLE")


    def get_singular_inference_time(self):
        if self.single_sample_input == None:
            raise Exception("THERE IS AN ABSENSE OF A SINGLE EXAMPLE; PLEASE COMPILE")
        serial = self.time_manager.start_job('singular_inference')

    def get_batch_inference_time(self):
        if self.single_sample_input == None:
            raise Exception("THERE IS AN ABSENSE OF A BATCH EXAMPLE; PLEASE COMPILE")
        serial = self.time_manager.start_job('batch_inference')
        
    

