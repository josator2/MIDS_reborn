class tagger():
    # scan group
    #               SE = Spin Echo          =====>>>> 'SE'
    #               IR = Inversion Recovery =====>>>> 'IR' 'IR\\SE' 'SE\\IR'
    #               GR = Gradient Recalled  =====>>>> 'GR'
    #               EP = Echo Planar        =====>>>> 'EP' 'EP\\SE' 'EP\\SE\\EP' 'EP\\S'
    #               RM = Research Mode      =====>>>> 'RM'


    def __init__(self, dict_atrubutes, dict_tags):


        self.ScanSeq = [['SE'], ['IR', 'IR\\SE', 'SE\\IR'], ['GR', 'GR\\IR', 'IR\\GR', 'EP\\GR'],
                   ['EP', 'EP\\SE', 'EP\\SE\\EP', 'EP\\S', 'EP\\G', 'EP\\IR'], ['RM']]
        self.Scan

    def load_table_protocol(self, protocol_table_path):
        pd.read_csv(protocol_table_path, sep='\t', index=False)