import numpy as np
import pandas as pd


def RA_process(folder_path):
    
    RA_path = folder_path + '\\RA.pickle.gz'
    RA_df = pd.read_pickle(RA_path)
    # Convert cột Key id$JyoCD
    RA_df['id$JyoCD'] = RA_df['id$JyoCD'].astype('int64')

    # Tạo cột Year
    RA_df['Year'] = RA_df['id$Year']
    # Tạo cột Month
    RA_df['Month'] = RA_df['id$MonthDay'].apply(lambda x: int(x/100))
    RA_df[['Month', 'id$MonthDay']][RA_df['Month']==12]
    # Tổng hợp giải thưởng trước trận đấu
    syokinAfter = [ 'Honsyokin$1',                
                   'Honsyokin$2',               
                'Honsyokin$3',                
                'Honsyokin$4',
                'Honsyokin$5',
                'Fukasyokin$1',
                'Fukasyokin$2',
                'Fukasyokin$3'
             ]
    syokinBefore = [ 'HonsyokinBefore$1',                
                     'HonsyokinBefore$2',               
                    'HonsyokinBefore$3',                
                    'HonsyokinBefore$4',
                    'HonsyokinBefore$5',
                    'FukasyokinBefore$1',
                    'FukasyokinBefore$2',
                    'FukasyokinBefore$3'
                   ]

    for after, before in zip(syokinAfter, syokinBefore):
        #print(after, before)
        RA_df.loc[RA_df[before]!=0, after] = RA_df[before]
    # Tạo cột mới
    RA_df['Honsyokin'] = RA_df['Honsyokin$1'] + RA_df['Honsyokin$2'] + RA_df['Honsyokin$3'] + RA_df['Honsyokin$4'] + RA_df['Honsyokin$5']
    RA_df['Fukasyokin'] = RA_df['Fukasyokin$1'] + RA_df['Fukasyokin$2'] + RA_df['Fukasyokin$3']
    
    # Select columns
    selected_columns =  ['id$Year',
                        'id$MonthDay',
                        'id$JyoCD',
                        'id$Kaiji',
                        'id$Nichiji',
                        'id$RaceNum',
                        'Year',
                        'Month',
                        'RaceInfo$TokuNum',
                        'RaceInfo$Nkai',
                        'GradeCD',
                        'JyokenInfo$SyubetuCD',
                        'JyokenInfo$KigoCD',
                        'JyokenInfo$JyuryoCD',
                        'Kyori', 
                        'TrackCD',
                        'TenkoBaba$TenkoCD',
                        'TenkoBaba$SibaBabaCD',
                        'TenkoBaba$DirtBabaCD',
                        'Honsyokin',
                        'Fukasyokin',
                      ]
    RA_df = RA_df[selected_columns]
    
    return RA_df


def SE_process(folder_path):
    
    SE_path = folder_path + '\\SE.pickle.gz'
    SE_df = pd.read_pickle(SE_path)
    # Convert cột Key id$JyoCD
    SE_df['id$JyoCD'] =SE_df['id$JyoCD'].astype('int64')
 
    selected_columns =  [
                            #Key
                            'id$Year',
                            'id$MonthDay',
                            'id$JyoCD',
                            'id$Kaiji',
                            'id$Nichiji',
                            'id$RaceNum',
                            #
                            'Umaban', 
                            'KettoNum',
                            'UmaKigoCD',
                            'SexCD',
                            'HinsyuCD',
                            'KeiroCD',
                            'Barei',
                            'TozaiCD',
                            'ChokyosiCode',
                            'BanusiCode',
                            'Futan',
                            'KisyuCode',
                            'MinaraiCD',
                            'BaTaijyu',
                            'ZogenFugo',
                            'ZogenSa',
                            'IJyoCD',
                            'KakuteiJyuni',
                            'Time',
                            'Odds',
                            'TimeDiff'
                           ]
    SE_df = SE_df[selected_columns]
    SE_df.reset_index(drop=True, inplace=True)
    return SE_df


def UM_process(folder_path):
    
    UM_path = folder_path + '\\UM.pickle.gz'
    UM_df = pd.read_pickle(UM_path)
    
    # Select Columns
    selected_columns =  [
                            'KettoNum',
                            'Bamei',
                            'ZaikyuFlag',
                            'SexCD',
                            'HinsyuCD',
                            'KeiroCD',
                            'Ketto3Info$1$HansyokuNum',
                            'Ketto3Info$1$Bamei',
                            'TozaiCD',
                            'ChokyosiCode',
                            'BreederCode',  #
                            'BanusiCode',
                            'RuikeiHonsyoHeiti',
                            'RuikeiHonsyoSyogai',
                            'RuikeiFukaHeichi',
                            'RuikeiFukaSyogai',
                            'RuikeiSyutokuHeichi',
                            'RuikeiSyutokuSyogai',
                            ]
    UM_df = UM_df[selected_columns]
    # Đổi tên các cột 
    for column in selected_columns:
        if column != 'KettoNum':
            new_column = 'UM_' + column
            UM_df.rename(columns={column: new_column}, inplace=True)
            
    UM_df.reset_index(drop=True, inplace=True)
    
    return UM_df


def KS_process(folder_path):
    
    KS_path = folder_path + '\\KS.pickle.gz'
    KS_df = pd.read_pickle(KS_path)
    
    # Select Columns
    select_columns =  [
                        'KisyuCode',
                        'SexCD',
                        'SikakuCD',
                        'MinaraiCD',
                        'TozaiCD',
                        'Syotai',
                        'ChokyosiCode',
                        #'SaikinJyusyo$1$GradeCD',
                        #'SaikinJyusyo$2$GradeCD',
                        #'SaikinJyusyo$3$GradeCD',
                     ]
    KS_df = KS_df[select_columns]
    # Đổi tên các cột TozaiCD thành KS_TozaiCD
    for column in select_columns:
        if column != 'KisyuCode':
            new_column = 'KS_' + column
            KS_df.rename(columns={column: new_column}, inplace=True)
    
            
    KS_df.reset_index(drop=True, inplace=True)
    
    return KS_df


def CH_process(folder_path):
    
    CH_path = folder_path + '\\CH.pickle.gz'
    CH_df = pd.read_pickle(CH_path)
    CH_df.drop_duplicates(subset=['ChokyosiCode'], keep='first', inplace=True)
    
    select_columns =  [
                            'ChokyosiCode',
                            'SexCD',
                            'TozaiCD',
                            'Syotai',
                            #'SaikinJyusyo$1$GradeCD',
                            #'SaikinJyusyo$2$GradeCD',
                            #'SaikinJyusyo$3$GradeCD',
                         ]
    CH_df = CH_df[select_columns]
    # Đổi tên các cột TozaiCD thành CH_TozaiCD
    for column in select_columns:
        if column != 'ChokyosiCode':
            new_column = 'CH_' + column
            CH_df.rename(columns={column: new_column}, inplace=True)
               
    CH_df.reset_index(drop=True, inplace=True)
    
    return CH_df


def HN_process(folder_path):
    
    HN_path = folder_path + '\\HN.pickle.gz'
    HN_df = pd.read_pickle(HN_path)
    HN_df.drop_duplicates(subset=['HansyokuNum'], keep='first', inplace=True)
    
    selected_columns =  [
                            'HansyokuNum',
                            #'KettoNum',
                            'Bamei',
                            'SexCD',
                            'HinsyuCD',
                            'KeiroCD',
                            'HansyokuMochiKubun',
                            'HansyokuFNum',
                            'HansyokuMNum',
                            ]
    HN_df = HN_df[selected_columns]
    # Đổi tên các cột 
    for column in selected_columns:
        if column != 'HansyokuNum':
            new_column = 'HN_' + column
            HN_df.rename(columns={column: new_column}, inplace=True)
               
    HN_df.reset_index(drop=True, inplace=True)
    
    return HN_df

def create_new_race_data(folder_path):
    # Load tables
    RA_df = RA_process(folder_path)
    SE_df = SE_process(folder_path)
    UM_df = UM_process(folder_path)
    KS_df = KS_process(folder_path)
    CH_df = CH_process(folder_path)
    HN_df = HN_process(folder_path)
        
    # Merge tables
    UM_df['HansyokuNum'] = UM_df['UM_Ketto3Info$1$HansyokuNum']
    # Merge 2 table UM, HN
    UM_HN_df = pd.merge(UM_df, HN_df, on=['HansyokuNum'], how='left')
    # 
    UM_HN_SE_df = pd.merge(SE_df, UM_HN_df, on=['KettoNum'], how='left')
    #
    UM_HN_SE_KS_df = pd.merge(UM_HN_SE_df, KS_df, on=['KisyuCode'], how='left')
    #
    UM_HN_SE_KS_CH_df = pd.merge(UM_HN_SE_KS_df, CH_df, on=['ChokyosiCode'], how='left')
    #
    UM_HN_SE_KS_CH_RA_df = pd.merge(RA_df, UM_HN_SE_KS_CH_df, on=['id$Year', 'id$MonthDay', 'id$JyoCD', 'id$Kaiji', 'id$Nichiji', 'id$RaceNum'], how='left')
    final_df = UM_HN_SE_KS_CH_RA_df.copy()
    
    # Update information from WE and WH tables
    WE_df = pd.read_pickle(folder_path+'\\WE.pickle.gz')
    WE_df = WE_df.loc[WE_df['id$JyoCD']==RA_df['id$JyoCD'].values[0], :]
    
    final_df['TenkoBaba$TenkoCD'] = WE_df['TenkoBaba$TenkoCD'].values[0]
    final_df['TenkoBaba$SibaBabaCD'] = WE_df['TenkoBaba$SibaBabaCD'].values[0]
    final_df['TenkoBaba$DirtBabaCD'] = WE_df['TenkoBaba$DirtBabaCD'].values[0]
    
    WH_df = pd.read_pickle(folder_path+'\\WH.pickle.gz')
    BaTaijyu_list = []
    ZogenFugo_list = []
    ZogenSa_list= []
    for i in range(1, len(SE_df)+1):
        BaTaijyu_col = 'BataijyuInfo$' + str(i) + '$BaTaijyu'
        BaTaijyu_list.append(WH_df[BaTaijyu_col].values[0])
        ZogenFugo_col = 'BataijyuInfo$' + str(i) + '$ZogenFugo'
        ZogenFugo_list.append(WH_df[ZogenFugo_col].values[0])
        ZogenSa_col = 'BataijyuInfo$' + str(i) + '$ZogenSa'
        ZogenSa_list.append(WH_df[ZogenSa_col].values[0])
        
    final_df['BaTaijyu'] = BaTaijyu_list
    final_df['ZogenFugo'] = ZogenFugo_list
    final_df['ZogenSa'] = ZogenSa_list
    
    # Convert  ZogenSa 
    final_df.loc[final_df['ZogenSa']=='   ', 'ZogenSa'] = 0
    final_df['ZogenSa'] = final_df['ZogenSa'].astype('float64')
    final_df.loc[final_df['ZogenFugo']=='-', 'ZogenSa'] = -1 * final_df['ZogenSa']
    final_df['ZogenSa']
    
    # Remove trường hợp BaTaijyu = 0 vì bị cancel start
    final_df = final_df[final_df['BaTaijyu']!=0]
    final_df.reset_index(drop=True, inplace=True)
    # Drop ZogenFugo
    final_df.drop('ZogenFugo', axis=1, inplace=True)
   
    # Select columns
    import json
    with open('..\\processes\\model_and_improve\\feature_dict_all.json') as js:
        feature_dict = json.load(js)
    cat_col = feature_dict['cat_col']
    num_col = feature_dict['num_col']
    ref_col = feature_dict['ref_col']
    
    id_col = ['KettoNum']
    columns = id_col + cat_col + num_col + ref_col
    test_data  = final_df[columns]
    
    return test_data