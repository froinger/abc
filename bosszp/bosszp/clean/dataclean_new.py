import pandas as pd
from sqlalchemy import create_engine
import logging

# 读取 file.csv 文件
all_city_zp_df = pd.read_csv('../../file.csv', encoding='utf8')

# 对重复行进行清洗。
all_city_zp_df.drop_duplicates(inplace=True)

# 对`工作地址`字段进行预处理。要求：北京·海淀区·西北旺 --> 北京，海淀区，西北旺。分隔成3个字段
all_city_zp_area_df = all_city_zp_df['job_location'].str.split('·', expand=True)
all_city_zp_area_df = all_city_zp_area_df.rename(columns={0: "city", 1: "district", 2: "street"})

# 对`薪资`字段进行预处理。要求：30-60K·15薪 --> 最低：30，最高：60
all_city_zp_salary_df = all_city_zp_df['job_salary_range'].str.split('K', expand=True)[0].str.split('-', expand=True)
all_city_zp_salary_df = all_city_zp_salary_df.rename(columns={0: 'salary_lower', 1: 'salary_high'})

def fun_work_year(x):
    if x in "1-3年":
        return 1
    elif x in "3-5年":
        return 2
    elif x in "5-10年":
        return 3
    elif x in "10年以上":
        return 4
    else:
        return 0


all_city_zp_df['job_experience'] = all_city_zp_df['job_experience'].apply(lambda x: fun_work_year(x))

# 对`企业规模`字段进行预处理。要求：500人以下：0，500-999：1，1000-9999：2，10000人以上：3
def fun_com_size(x):
    if x in "500-999人":
        return 1
    elif x in "1000-9999人":
        return 2
    elif x in "10000人以上":
        return 3
    else:
        return 0


# 对`岗位福利`字段进行预处理。要求：将描述中的中文'，'（逗号）,替换成英文','（逗号）
all_city_zp_df['job_welfare'] = all_city_zp_df['job_welfare'].str.replace('，', ',')

#对‘招收人数’字段进行预处理。
all_city_zp_salary_df = all_city_zp_df['job_scale'].str.split('人', expand=True)[0].str.split('-', expand=True)
all_city_zp_salary_df = all_city_zp_salary_df.rename(columns={0: 'scale_lower', 1: 'scale_high'})

# 合并所有数据集
clean_all_city_zp_df = pd.concat([all_city_zp_df, all_city_zp_salary_df, all_city_zp_area_df], axis=1)

# 删除冗余列
clean_all_city_zp_df.drop('job_location', axis=1, inplace=True)  # 删除原区域
clean_all_city_zp_df.drop('job_salary_range', axis=1, inplace=True)  # 删除原薪资
clean_all_city_zp_df.drop('job_scale',axis=1,inplace=True)  #删除原人数

# 对缺失值所在行进行清洗。
clean_all_city_zp_df.dropna(axis=0, how='any', inplace=True)
clean_all_city_zp_df.drop(axis=0,
                          index=(clean_all_city_zp_df.loc[(clean_all_city_zp_df['job_welfare'] == 'None')].index),
                          inplace=True)
# 将处理后的数据保存到 MySQL 数据库
engine = create_engine('mysql+pymysql://player:BvXXbGtR4uFxCBrMmbfN@117.72.35.68:3306/spider_db?charset=utf8')
clean_all_city_zp_df.to_sql('t_boss_zp_info', con=engine, if_exists='replace')
logging.info("Write to MySQL Successfully!")