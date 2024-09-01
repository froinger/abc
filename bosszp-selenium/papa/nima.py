import mysql.connector
import pandas as pd

# 连接到MySQL数据库
conn = mysql.connector.connect(
    host='117.72.35.68',         # 替换为你的主机地址
    user='root',     # 替换为你的用户名
    password='UiiWz5mAdmiygwAbAFem', # 替换为你的密码
    database='spider_db'  # 替换为你的数据库名称
)

# 查询表数据
query = "SELECT * FROM t_boss_zp_info"  # 替换为你的表名称
df = pd.read_sql(query, conn)

# 将数据导出为CSV文件
df.to_csv('./washed.csv', index=False)

# 关闭数据库连接
conn.close()
