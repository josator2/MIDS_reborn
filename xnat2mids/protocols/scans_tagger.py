import pandas as pd
import numpy as np
class Tagger:
    # scan group
    #               SE = Spin Echo          =====>>>> 'SE'
    #               IR = Inversion Recovery =====>>>> 'IR' 'IR\\SE' 'SE\\IR'
    #               GR = Gradient Recalled  =====>>>> 'GR'
    #               EP = Echo Planar        =====>>>> 'EP' 'EP\\SE' 'EP\\SE\\EP' 'EP\\S'
    #               RM = Research Mode      =====>>>> 'RM'


    def __init__(self):

        self.ScanSeq = [['SE'], ['IR', 'IR\\SE', 'SE\\IR'], ['GR', 'GR\\IR', 'IR\\GR', 'EP\\GR'],
                   ['EP', 'EP\\SE', 'EP\\SE\\EP', 'EP\\S', 'EP\\G', 'EP\\IR'], ['RM']]


    def load_table_protocol(self, protocol_table_path):
        self.table_protocols = pd.read_csv(protocol_table_path, sep='\t',index_col= False)

    def classification_by_min_max(self, dict_atrubutes):

        #targetScan = pd.DataFrame.from_dict([dict_atrubutes])
        # Verify to which scan group corresponds
        scaning_sequence = dict_atrubutes["Scanning Sequence ('00180020')"]
        scaning_sequence = scaning_sequence if type(scaning_sequence) is str else "\\".join(scaning_sequence)
        table_protocol_SS = self.table_protocols[[
                    (False if scaning_sequence not in l else True)
                    for l in list(self.table_protocols["Scanning Sequence ('00180020')"])
                ]]
        #print(table_protocol_SS)

        #for pix in table_protocol_SS.index():
        matrix = []
        adquisition_param_keys = list(dict_atrubutes.keys())[-5:]
        for p in adquisition_param_keys:
            distance = []
            #print("p_value", dict_atrubutes[p], type(dict_atrubutes[p]))
            p_value = float(dict_atrubutes[p]) if dict_atrubutes[p] !="nan" else -1
            for list_values in table_protocol_SS[p]:
                #print(p, list_values)
                min_ = np.amin(eval(list_values))
                max_ = np.amax(eval(list_values))
                if p_value >= min_ and p_value<=max_: distance.append(np.sum([0., 0.]))
                else: distance.append(np.sum([abs(p_value-min_), abs(p_value-max_)]))
            matrix.append(distance)
        pos_table_protocol = np.argmin(np.array(matrix).sum(axis=0))
        return table_protocol_SS.iloc[pos_table_protocol][["Protocol","acq","folder"]]