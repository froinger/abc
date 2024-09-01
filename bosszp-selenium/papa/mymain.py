#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : jhzhong
# @time    : 2023/12/22 8:23
# @function: the script is used to do something.
# @version : V1
import datetime
import time
from selenium import webdriver
from papa_service.api.dbutils import DBUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# 前情提要：不要开代理

def wait_for_user():
    input("请手动完成操作后在控制台输入 'ok' 继续: ")


def login(browser):
    # 打开登录页面
    login_url = 'https://login.zhipin.com'
    browser.get(login_url)
    input("请登录完成后在控制台输入 'ok' 继续: ")
    time.sleep(1)


def retry_on_failure(max_retries, function, *args, **kwargs):
    retries = 0
    while retries < max_retries:
        try:
            return function(*args, **kwargs)
        except (StaleElementReferenceException, TimeoutException) as e:
            retries += 1
            print(f"Error: {e}. Retrying {retries}/{max_retries}...")
            time.sleep(1)
    raise Exception(f"Failed after {max_retries} retries")


if __name__ == "__main__":
    print("启动爬虫...")

    browser = webdriver.Edge()
    login(browser)

    # 建立数据库连接
    print("正在连接数据库...")
    db = DBUtils('117.72.35.68', 'root', 'UiiWz5mAdmiygwAbAFem', 'spider_db')
    print("数据库连接成功！")

    index_url = 'https://www.zhipin.com/?city=100010000&ka=city-sites-100010000'
    city_map = {
        "北京": ["北京"],
        "天津": ["天津"],
        "山西": ["太原", "阳泉", "晋城", "长治", "临汾", "运城", "忻州", "吕梁", "晋中", "大同", "朔州"],
        "河北": ["沧州", "石家庄", "唐山", "保定", "廊坊", "衡水", "邯郸", "邢台", "张家口", "辛集", "秦皇岛", "定州",
                 "承德", "涿州"],
        "山东": ["济南", "淄博", "聊城", "德州", "滨州", "济宁", "菏泽", "枣庄", "烟台", "威海", "泰安", "青岛", "临沂",
                 "莱芜", "东营", "潍坊", "日照"],
        "河南": ["郑州", "新乡", "鹤壁", "安阳", "焦作", "濮阳", "开封", "驻马店", "商丘", "三门峡", "南阳", "洛阳",
                 "周口",
                 "许昌", "信阳", "漯河", "平顶山", "济源"],
        "广东": ["珠海", "中山", "肇庆", "深圳", "清远", "揭阳", "江门", "惠州", "河源", "广州", "佛山", "东莞", "潮州",
                 "汕尾", "梅州", "阳江", "云浮", "韶关", "湛江", "汕头", "茂名"],
        "浙江": ["舟山", "温州", "台州", "绍兴", "衢州", "宁波", "丽水", "金华", "嘉兴", "湖州", "杭州"],
        "宁夏": ["中卫", "银川", "吴忠", "石嘴山", "固原"],
        "江苏": ["镇江", "扬州", "盐城", "徐州", "宿迁", "无锡", "苏州", "南通", "南京", "连云港", "淮安", "常州",
                 "泰州"],
        "湖南": ["长沙", "邵阳", "怀化", "株洲", "张家界", "永州", "益阳", "湘西", "娄底", "衡阳", "郴州", "岳阳",
                 "常德",
                 "湘潭"],
        "吉林": ["长春", "长春", "通化", "松原", "四平", "辽源", "吉林", "延边", "白山", "白城"],
        "福建": ["漳州", "厦门", "福州", "三明", "莆田", "宁德", "南平", "龙岩", "泉州"],
        "甘肃": ["张掖", "陇南", "兰州", "嘉峪关", "白银", "武威", "天水", "庆阳", "平凉", "临夏", "酒泉", "金昌",
                 "甘南",
                 "定西"],
        "陕西": ["榆林", "西安", "延安", "咸阳", "渭南", "铜川", "商洛", "汉中", "宝鸡", "安康"],
        "辽宁": ["营口", "铁岭", "沈阳", "盘锦", "辽阳", "锦州", "葫芦岛", "阜新", "抚顺", "丹东", "大连", "朝阳",
                 "本溪",
                 "鞍山"],
        "江西": ["鹰潭", "宜春", "上饶", "萍乡", "南昌", "景德镇", "吉安", "抚州", "新余", "九江", "赣州"],
        "黑龙江": ["伊春", "七台河", "牡丹江", "鸡西", "黑河", "鹤岗", "哈尔滨", "大兴安岭", "绥化", "双鸭山",
                   "齐齐哈尔",
                   "佳木斯", "大庆"],
        "安徽": ["宣城", "铜陵", "六安", "黄山", "淮南", "合肥", "阜阳", "亳州", "安庆", "池州", "宿州", "芜湖",
                 "马鞍山",
                 "淮北", "滁州", "蚌埠"],
        "湖北": ["孝感", "武汉", "十堰", "荆门", "黄冈", "襄阳", "咸宁", "随州", "黄石", "恩施", "鄂州", "荆州", "宜昌",
                 "潜江", "天门", "神农架", "仙桃"],
        "青海": ["西宁", "海西", "海东", "玉树", "黄南", "海南", "海北", "果洛"],
        "新疆": ["乌鲁木齐", "克州", "阿勒泰", "五家渠", "石河子", "伊犁", "吐鲁番", "塔城", "克拉玛依", "喀什", "和田",
                 "哈密", "昌吉", "博尔塔拉", "阿克苏", "巴音郭楞", "阿拉尔", "图木舒克", "铁门关"],
        "贵州": ["铜仁", "黔东南", "贵阳", "安顺", "遵义", "黔西南", "黔南", "六盘水", "毕节"],
        "四川": ["遂宁", "攀枝花", "眉山", "凉山", "成都", "巴中", "广安", "自贡", "甘孜", "资阳", "宜宾", "雅安",
                 "内江",
                 "南充", "绵阳", "泸州", "凉山", "乐山", "广元", "甘孜", "德阳", "达州", "阿坝"],
        "上海": ["上海"],
        "广西": ["南宁", "贵港", "玉林", "梧州", "钦州", "柳州", "来宾", "贺州", "河池", "桂林", "防城港", "崇左",
                 "北海",
                 "百色"],
        "西藏": ["拉萨", "山南", "日喀则", "那曲", "林芝", "昌都", "阿里"],
        "云南": ["昆明", "红河", "大理", "玉溪", "昭通", "西双版纳", "文山", "曲靖", "普洱", "怒江", "临沧", "丽江",
                 "红河",
                 "迪庆", "德宏", "大理", "楚雄", "保山"],
        "内蒙古": ["呼和浩特", "乌兰察布", "兴安", "赤峰", "呼伦贝尔", "锡林郭勒", "乌海", "通辽", "巴彦淖尔", "阿拉善",
                   "鄂尔多斯", "包头"],
        "海南": ["海口", "三沙", "三亚", "临高", "五指山", "陵水", "文昌", "万宁", "白沙", "乐东", "澄迈", "屯昌",
                 "定安",
                 "东方", "保亭", "琼中", "琼海", "儋州", "昌江"],
        "重庆": ["重庆"]
    }
    browser.get(index_url)

    show_ele = browser.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b')
    actions = ActionChains(browser)
    today = datetime.date.today().strftime('%Y-%m-%d')
    # 这玩意定义第几个分类，也是左闭右开，如[43,44]表示只遍历第43个分类。
    # 每次爬10比较好控制，多的话人要在边上处理人机验证，不过目前逻辑也是逐渐优化得可以连续验证了。
    # 一共的话是85个分类。
    from_to=[51,85]



    # 现在已爬好到50，明天直接跑即可

    i=from_to[0]
    # 神秘python特性之左闭右开，因此我直接采用while循环，轻松控制左右都为闭区间。
    # for i in range(from_to[0], from_to[1]):
    while i<=from_to[1]:
        print(f"正在处理第 {i} 个分类（咱程序员喜欢从0开始数你懂得...）")

        try:
            max_retries = 3
            retries = 0
            while retries < max_retries:
                try:
                    actions.move_to_element(show_ele).perform()
                    time.sleep(1)
                    elements = retry_on_failure(max_retries, browser.find_elements, By.XPATH,
                                                '//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/div/ul/li/div/a')
                    current_a = elements[i]

                    current_category = retry_on_failure(max_retries, current_a.find_element, By.XPATH,
                                                        '../../h4').text.strip()

                    sub_category = current_a.text.strip()

                    if current_category and sub_category:
                        break
                    else:
                        print(f"分类或子分类为空，重试 {retries+1} 次...")
                        retries += 1
                        time.sleep(1)

                except (StaleElementReferenceException, TimeoutException) as e:
                    print(f"Error retrieving category or sub-category: {e}")
                    retries += 1
                    time.sleep(1)

            if retries == max_retries:
                print(f"跳过此项：无法获取分类或子分类 (第 {i + 1} 次尝试)")
                continue

            print(f"{today} 正在抓取 {current_category} -- {sub_category}")
            retry_on_failure(max_retries, browser.execute_script, "arguments[0].click();", current_a)

            try:
                time.sleep(5)

                print(f"正在滚动页面以加载更多职位...")
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except Exception as e:
                print(f"Error while scrolling: {e}")
                wait_for_user()

            print(f"正在提取 {current_category} -- {sub_category} 下的职位信息...")
            job_detail = browser.find_elements(By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/ul/li')
            for job in job_detail:
                try:
                    job_title = retry_on_failure(max_retries, job.find_element, By.XPATH,
                                                 "./div[1]/a/div[1]/span[1]").text.strip()
                    job_location = job.find_element(By.XPATH, "./div[1]/a/div[1]/span[2]/span").text.strip()
                    job_company = job.find_element(By.XPATH, "./div[1]/div/div[2]/h3/a").text.strip()
                    job_industry = job.find_element(By.XPATH, "./div[1]/div/div[2]/ul/li[1]").text.strip()
                    job_finance = job.find_element(By.XPATH, "./div[1]/div/div[2]/ul/li[2]").text.strip()
                    job_scale = job.find_element(By.XPATH,
                                                 "./div[1]/div/div[2]/ul/li[3]").text.strip() if job.find_elements(
                        By.XPATH, "./div[1]/div/div[2]/ul/li[3]") else "无"
                    job_welfare = job.find_element(By.XPATH, "./div[2]/div").text.strip() if job.find_elements(By.XPATH,
                                                                                                               "./div[2]/div") else '无'
                    job_salary_range = job.find_element(By.XPATH, "./div[1]/a/div[2]/span[1]").text.strip()
                    job_experience = job.find_element(By.XPATH, "./div[1]/a/div[2]/ul/li[1]").text.strip()
                    job_education = job.find_element(By.XPATH, "./div[1]/a/div[2]/ul/li[2]").text.strip()
                    job_skills = ','.join([skill.text.strip() for skill in
                                           job.find_elements(By.XPATH, "./div[2]/ul/li")]) if job.find_elements(
                        By.XPATH, "./div[2]/ul/li") else '无'
                    city = job_location.split('·')[0]
                    province = next((p for p, cities in city_map.items() if city in cities), '')

                    print(f"职位: {job_title}, 公司: {job_company}, 地点: {job_location}, 工资: {job_salary_range}"
                          f", 经验: {job_experience}, 学历: {job_education}, 技能: {job_skills}"
                          f", 行业: {job_industry}, 融资: {job_finance}, 规模: {job_scale}, 福利: {job_welfare}"
                          f", 省份: {province}")

                    db.insert_data(
                        "insert into job_info(category, sub_category, job_title, province, job_location, job_company, job_industry, job_finance, job_scale, job_welfare, job_salary_range, job_experience, job_education, job_skills, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        args=(
                            current_category, sub_category, job_title, province, job_location, job_company,
                            job_industry,
                            job_finance, job_scale, job_welfare, job_salary_range, job_experience, job_education,
                            job_skills, today))

                except Exception as e:
                    print(f"Error processing job: {e}")

            print(f"{current_category} -- {sub_category} 下的职位信息提取完成。")

            try:
                browser.get(index_url)
                show_ele = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b'))
                )
                show_ele.click()


            except Exception as e:
                print(f"Error returning to main page: {e}")
                browser.get(index_url)
                show_ele = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b'))
                )
                show_ele.click()

        except Exception as e:
            print(f"Error processing category: {e}")
            print(f"当前在第 {i} 个分类出现报错...")
            wait_for_user()
            # 以下操作是必须的，人机验证之后。
            browser.get(index_url)
            show_ele = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/dl[1]/dd/b'))
            )
            show_ele.click()
            continue

        print(f"第 {i} 个分类处理完成，等待2秒...")
        i += 1
        time.sleep(2)

    print("所有分类处理完成，爬虫结束。")
    time.sleep(10)
