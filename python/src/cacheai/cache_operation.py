import argparse

import sys
import os
import numpy as np

import cv2
import matplotlib.pyplot as plt
import math
import time

from PIL import Image, ImageDraw, ImageFont
import ggutils.s3_access as s3_access

import smalltrain as st
from smalltrain.model.operation import Operation
from smalltrain.utils.tf_util import SavedModel

from cacheai.utils import image_util
from cacheai.db import CacheDB
from cacheai.manager.cache_manager import CacheManager
from cacheai.utils import hash_util


class CacheAIOperation(Operation):
    '''Operation class as hyper parameter of train or prediction operation
    Arguments:
        params: A dictionary that maps hyper parameter keys and values
        debug_mode: Boolean, if `True` then running with debug mode.
    '''

    def __init__(self, hparams=None, setting_file_path=None):
        super().__init__(hparams, setting_file_path)
        print('CacheAIOperation init hparams_dict: {}'.format(self.hparams_dict))

        self.debug_mode = True
        self.prediction_mode = False

        self.label_character_dict = image_util.get_label_character_dict()
        # print('label_character_dict: {}'.format(self.label_character_dict))
        self.character_label_dict = {v: k for k, v in self.label_character_dict.items()}

        self.model_id = 'SCR'
        self.cache_input_layer_name = self.hparams_dict.get('cache_input_layer_name')
        # self.cache_output_layer_name = 'model/fc/output_middle_layer'
        self.cache_output_layer_name = 'model/output'
        print('CacheAIOperation init cache_input_layer_name: {}'.format(self.cache_input_layer_name))

    def test(self, img_file_path):
        # TODO test with splitted models
        return

        test_img = cv2.imread(img_file_path)
        print('test_img: {}'.format(test_img))
        output = self.predict(input=test_img)
        label = np.argmax(output)
        detected_character = self.label_character_dict.get(label)
        print('detected_character: {}'.format(detected_character))

    def predict(self, input):
        saved_model_dir_path = self.hparams_dict.get('saved_model_dir_path')
        if saved_model_dir_path:
            print('predict by saved model')
            output = self.saved_model.predict_single_data(input)
        else:
            print('predict by restored model')
            output = self.model.predict_single_data(input)
        print('Predicted output: {}'.format(output))
        return output

    def create_cache_manager(self):
        manager = CacheManager(model_ins=self.model, model_id=self.model_id,
                               cache_input_layer_name=self.cache_input_layer_name,
                               cache_output_layer_name=self.cache_output_layer_name)
        print('get_cache_size: {}'.format(manager.get_cache_size()))
        self.manager = manager
        return manager

    def test_generate_text_matrix_image(self, target_character='日', rotate_angle=5):
        img, text_matrix, whole_img = image_util.generate_text_matrix_image(character=target_character,
                                                                            rotate_angle=rotate_angle)
        print('generate_text_matrix_image: {}, target_character: {}'.format(text_matrix, target_character))

    def bench(self, iterr=None, with_cache=False, target_character_list=['日'], manager=None):

        manager = manager or self.create_cache_manager()

        input_hash_dict = {}
        cache_dict = {}

        sources = 2 ** 8

        total_cnt = 0
        accurate_cnt = 0

        # Check character_label_dict
        for target_character in target_character_list:
            _label = self.character_label_dict.get(target_character)
            print('target_character: {}, _label: {}'.format(target_character, _label))

        print('iterr: {}'.format(iterr))
        if iterr is None:
            # rotate_angle_list = list(range(-3, 3))
            # rotate_angle_list = [0] * 10
            # width_list = list(range(31, 34))
            # width_list = [32] * 3
            rotate_angle_list = [0]

            width_list = list(range(31, 34))
            # tx_list = list(range(-3, 3))
            # ty_list = list(range(-3, 3))
            tx_list = list(range(-1, 1))
            ty_list = list(range(-1, 1))
            tx_list = list(range(-2, 2))
            ty_list = list(range(-2, 2))

            _debug_mode = False
            if _debug_mode:
                tx_list = [0]
                ty_list = [0]
                rotate_angle_list = [0]

            iterr = len(width_list) * len(tx_list) * len(ty_list) * len(rotate_angle_list) * len(target_character_list)

        else:
            rotate_angle_list = list(range(-5, 5))
            width_list = [32] * int(iterr / len(rotate_angle_list))
            tx_list = [0]
            ty_list = [0] * 32
            iterr = len(width_list) * len(tx_list) * len(ty_list) * len(rotate_angle_list) * len(target_character_list)
            print(len(width_list))
        print('iterr set: {}'.format(iterr))

        if not with_cache:
            # Export fc last layer
            target_character = target_character_list[0]
            img, _, _ = image_util.generate_text_matrix_image(character=target_character, width=width_list[0],
                                                              tx=0, ty=0, rotate_angle=0.0)
            _input_batch = [np.asarray(img)]
            W_fc_last_values = manager.model_ins.sess.run(
                manager.W_fc_last,
                feed_dict={manager.model_ins.x: _input_batch,
                           manager.model_ins.is_train: False,
                           manager.model_ins.keep_prob: 1}
            )
            print('W_fc_last_values.shape: {}'.format(W_fc_last_values.shape))
            _export_path = './W_fc_last_values.csv'
            np.savetxt(_export_path, W_fc_last_values, delimiter=",")
            _label = self.character_label_dict.get(target_character)
            _export_path = './W_fc_last_values_c{}.csv'.format(_label)
            np.savetxt(_export_path, W_fc_last_values[:, _label], delimiter=",")
            W_fc_last_values_label = W_fc_last_values[:, _label]
            W_fc_last_values_sorted = W_fc_last_values[:, _label].copy()
            W_fc_last_index_list = np.argsort(W_fc_last_values_sorted)[::-1]
            W_fc_last_values_sorted = np.asarray([[_index, W_fc_last_values_label[_index]] for _index in W_fc_last_index_list])
            print('W_fc_last_values_sorted.shape: {}'.format(W_fc_last_values_sorted.shape))
            _export_path = './W_fc_last_values_sorted_c{}.csv'.format(_label)
            np.savetxt(_export_path, W_fc_last_values_sorted, delimiter=",")

        sum_time_generate_text_matrix_image = 0
        sum_time_get_output = 0
        sum_lap_time_get_output = 0
        sum_lap_time_get_output_list = [0] * int(iterr / 100 + 1)

        start_time = time.time()
        for target_character in target_character_list:
            accurate_output = self.character_label_dict.get(target_character)

            for width in width_list:
                for tx in tx_list:
                    for ty in ty_list:
                        for rotate_angle in rotate_angle_list:
                            print('width: {}, tx: {}, ty: {}, rotate_angle: {}'.format(
                                width, tx, ty, rotate_angle))

                            start_time_generate_text_matrix_image = time.time()
                            # img = character_image(character=target_character, width=width, tx=x, ty=y, noise_source=noise_source)
                            img, _, _ = image_util.generate_text_matrix_image(character=target_character, width=width,
                                                                              tx=tx, ty=ty, rotate_angle=rotate_angle)
                            sum_time_generate_text_matrix_image += (time.time() - start_time_generate_text_matrix_image)

                            input_hash = hash_util.to_hash(np.asarray(img).reshape(-1).astype('int8'))

                            output_value = None
                            cache_key = None
                            info_value = {'input_hash': input_hash, 'output_value': output_value,
                                          'cache_key': cache_key,
                                          'cache_input_value': None,
                                          'character': target_character, 'rotate_angle': rotate_angle, 'width': width}

                            start_time_get_output = time.time()
                            if with_cache:
                                output_value, cache_key, cache_input_value = manager.get_output_from_cache(np.asarray(img))

                                info_value['cache_key'] = cache_key
                                cache_dict[cache_key] = input_hash
                                # Store also cache_input_value
                                info_value['cache_input_value'] = cache_input_value

                            else:
                                _input_batch = [np.asarray(img)]

                                output_value = manager.model_ins.sess.run(
                                    manager.cache_output_layer,
                                    feed_dict={manager.model_ins.x: _input_batch,
                                               manager.model_ins.is_train: False,
                                               manager.model_ins.keep_prob: 1}
                                )

                            _lap_time = (time.time() - start_time_get_output)
                            sum_time_get_output += _lap_time
                            sum_lap_time_get_output += _lap_time

                            # print('output_value: {}'.format(output_value))
                            # output_value = np.asarray(output_value).reshape(-1)[0]
                            output_value = output_value[0]
                            output_label = np.argmax(output_value, axis=0).astype(np.int)
                            output_character = self.label_character_dict.get(output_label)

                            info_value['output_value'] = output_value
                            info_value['output_label'] = output_label
                            info_value['output_character'] = output_character
                            # print('output_value: {}'.format(output_value))
                            if output_label == accurate_output:
                                accurate_cnt += 1
                            input_hash_dict[input_hash] = info_value

                            total_cnt += 1
                            if total_cnt % 100 == 0:
                                lap_time = time.time() - start_time

                                print(
                                    '{} % Done, spent  {} sec ({} sec/image) \n for generate_text_matrix_image {} sec/image \n for get_output {} sec/image'.format(
                                        100 * total_cnt / iterr,
                                        lap_time, lap_time / total_cnt,
                                        sum_time_generate_text_matrix_image / total_cnt,
                                        sum_time_get_output / total_cnt))
                                print('output_label: {}, output_character: {}, accurate_output: {}'.format(output_label, output_character, accurate_output))
                                print('width: {}, tx: {}, ty: {}, rotate_angle: {}'.format(width, tx, ty, rotate_angle))
                                print('=' * 20)

                                sum_lap_time_get_output_list[int(total_cnt / 100)] = sum_lap_time_get_output
                                sum_lap_time_get_output = 0

        total_time = time.time() - start_time
        print('{} % Done with total_time: {} sec'.format(100 * total_cnt / iterr, total_time))


        return input_hash_dict, cache_dict, accurate_cnt, total_cnt, sum_lap_time_get_output_list, total_time, sum_time_get_output


MODE_TEST = 'test'

# TEST_IMG_FILE_PATH = '/var/data/smalltrain-ocr/single_character/images/t花_c2016_w32_fipaexm-ttf_bNone_i0.jpg'
TEST_IMG_FILE_PATH = '/var/data/japanese-paper/images/t花_c2116_w32_fipaexg-ttf_b-var-data-japanese-paper-master-background-paper-paper_1-jpg_i0.jpg'

def main(exec_param):
    print(exec_param)
    operation = CacheAIOperation(setting_file_path=exec_param['setting_file_path'])
    mode = (exec_param['mode'] or MODE_TEST).lower() # Default mode
    print('exec_param: {}'.format(exec_param))
    operation_id = operation.hparams_dict.get("operation_id") or operation.hparams_dict.get("train_id")

    if exec_param.get('saved_model_dir_path'):
        operation.auto()
        operation.hparams_dict['saved_model_dir_path'] = exec_param['saved_model_dir_path']
        operation.saved_model = SavedModel(saved_model_dir_path=exec_param['saved_model_dir_path'])
    else:
        operation.auto()

    if mode == MODE_TEST:
        img_file_path = TEST_IMG_FILE_PATH
        operation.test(img_file_path=img_file_path)
        operation.create_cache_manager()
        operation.test_generate_text_matrix_image()

        with_cache = (operation.cache_input_layer_name is not None)

        print("=" * 10)
        print("with_cache: {}".format(with_cache))
        print("=" * 10)

        target_character_list = ['山', '川']
        target_character_list = ['9', 'あ']
        target_character_list = ['い', 'お']
        target_character_list = ['三', '田']
        target_character_list = ['沖', '縄', 'o', 'x']
        target_character_list = ['1', '2', '3', '4']
        target_character_list = ['０', 'か', 'き', 'く']
        target_character_list = ['け', 'こ']
        target_character_list = ['さ', 'し', 'す', 'せ', 'そ']
        target_character_list = ['擬', '態']
        target_character_list = ['5', '8']
        target_character_list = ['5', '6', '7', '8', '0']

        export_dir_path = "export/{}".format(operation_id)
        if operation.hparams_dict.get("cache_input_layer_name"):
            _layer_name_lists = [s for s in operation.hparams_dict["cache_input_layer_name"].split("/")
                                 if s.find("res_block") >= 0]
            if _layer_name_lists:
                export_dir_path = os.path.join(export_dir_path, _layer_name_lists[0])

        for target_character in target_character_list:
            input_hash_dict, hash_dict, accurate_cnt,\
            total_cnt, sum_lap_time_get_output_list, total_time, sum_time_get_output = operation.bench(
                iterr=None, with_cache=with_cache, target_character_list=[target_character])

            print("total_time: {}".format(total_time))
            print("sum_time_get_output: {}".format(sum_time_get_output))
            print("accurate_cnt: {}, total_cnt: {}".format(accurate_cnt, total_cnt))
            print("len of input_hash_dict: {}".format(len(input_hash_dict)))
            print("len of hash_dict: {}".format(len(hash_dict)))
            # export cache_input_value in input_hash_dict
            def expor_cache_input_value(input_hash_dict, dir_path="./export"):
                _len_input_hash_dict = len(input_hash_dict)
                _cache_input_value_array = None
                for i, input_hash in enumerate(input_hash_dict.keys()):
                    print("export i: {}, input_hash_dict with input_hash: {}".format(i, input_hash))
                    info_value = input_hash_dict[input_hash]
                    cache_input_value = info_value["cache_input_value"]
                    if cache_input_value is None:
                        continue
                    cache_input_value = np.asarray(cache_input_value)
                    cache_input_value = cache_input_value.reshape(-1)
                    cache_input_value = cache_input_value.astype(np.uint8)

                    if _cache_input_value_array is None:
                        _cache_input_value_array = np.zeros([_len_input_hash_dict, len(cache_input_value)], dtype=np.uint8)
                    _cache_input_value_array[i, :] = cache_input_value

                os.makedirs(dir_path, exist_ok=True)
                _export_path = os.path.join(dir_path, 'cache_input_value_c{}.csv'.format(target_character))

                np.savetxt(_export_path, _cache_input_value_array, delimiter=",")

                _max_value = _cache_input_value_array.max()
                _max_value = min(4, _max_value)
                print("_max_value: {}".format(_max_value))

                _gray_cache_input_value_array = _cache_input_value_array * 255.0 / _max_value
                _img_gray = Image.fromarray(np.uint8(_gray_cache_input_value_array))
                print("_img_gray _max_value: {}".format(_gray_cache_input_value_array))
                _export_path = os.path.join(dir_path, 'cache_input_value_c{}.png'.format(target_character))
                _img_gray.save(_export_path)

            def expor_output_character(input_hash_dict, dir_path="./export"):

                _len_input_hash_dict = len(input_hash_dict)
                output_character_list = [input_hash_dict[input_hash].get("output_character") for i, input_hash in enumerate(input_hash_dict.keys())]
                print("target_character: {},  output_character_list: {}".format(target_character, output_character_list))
                _export_array = np.asarray([output_character_list])

                os.makedirs(dir_path, exist_ok=True)
                _export_path = os.path.join(dir_path, 'output_character_c{}.csv'.format(target_character))
                np.savetxt(_export_path, _export_array, delimiter=",", encoding='utf8', fmt='%s')


            if input_hash_dict is not None or len(input_hash_dict) > 0:
                expor_cache_input_value(input_hash_dict, dir_path=export_dir_path)
                expor_output_character(input_hash_dict, dir_path=export_dir_path)

    else:
        raise ValueError('Invalid mode: {}'.format(mode))

    print('DONE main')

'''
Usage
OPERATION_ID=SCR_2D_CNN_V2_l49-c64_20220326-1756-PREDICTION

cd /var/smalltrain/cache-ai/src/python/
nohup python cacheai/cache_operation.py --setting_file_path=/var/smalltrain/operation/"$OPERATION_ID".json \
   > /var/smalltrain/logs/$OPERATION_ID.log 2>&1 &

'''
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='cache_operation')

    parser.add_argument('--mode', '-mmd', type=str, default=MODE_TEST,
                        help='String, The mode to exec(Default: {})'.format(MODE_TEST))
    parser.add_argument('--setting_file_path', '-sfp', type=str, default=None,
                        help='String, The setting file path of JSON String to set parameters')

    args = parser.parse_args()
    print('args:{}'.format(args))

    exec_param = vars(args)
    print('init exec_param:{}'.format(args))

    main(exec_param)
