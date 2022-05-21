from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import datetime
from selenium.webdriver.common.keys import Keys

import settings


class ScrapeElms:
    '''以下のELMSページでスクレイピングに関する処理を行うクラス
    ・https://www.elms.hokudai.ac.jp/portal/home/information/list

    Attributes
    ---------
        ID : string
            ユーザーID 
        PASSWORD : string
            パスワード
        select_index : int
            個人・グループ・個人宛以外のどれを選択するかを保持する変数
        time_stamp_list : list[`datetime`]
            タイムスタンプリスト
        title_list : list[`string`]
            タイトルリスト
        driver : 
            Chrome driver，スクレイピング操作に用いるドライバ
    '''

    def __init__(self, ID, PASSWORD):
        '''
        Parameters
        ----------
        ID : string
            ユーザーID
        PASSWORD : string
            パスワード
        '''
        
        self.ID = ID
        self.PASSWORD = PASSWORD
        self.select_index = 1
        self.time_stamp_list = []
        self.title_list = []

        # start up driver with headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install()) # start driver with gui mode

    def page_wait(self, class_name):
        '''ページのロードを待つ関数
        driver.get()の後などページの更新を待ちたい時に呼び出すとよい．
        
        Args
        ----
        class_name : string
            クラスの要素名を指定する．
        '''
        
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        # WebDriverWait(self.driver,
        #               15).until(EC.presence_of_all_elements_located) #これだと上手くロード待機できなかった
        

    def login(self):
        '''ログイン処理をする関数'''

        self.driver.get(
            "https://www.elms.hokudai.ac.jp/portal/home/information/list")
        self.page_wait("signin-button")  # wait for page loading

        id_input = self.driver.find_element_by_xpath("//input[@id='username_input']")
        id_input.send_keys(self.ID)
        password_input = self.driver.find_element_by_xpath("//input[@id='password_input']")
        password_input.send_keys(self.PASSWORD)

        login_button = self.driver.find_element_by_xpath("//input[@id='login_button']")
        login_button.send_keys(Keys.ENTER)  # push Enter
        # login_button.click() #なぜかチャットBOTの画像が押されてしまうのでEnterに変更


    def choose_dropdown_list(self, index):
        '''ドロップダウンリスト(個人・グループ・個人宛以外)から一つを選択する
        Args
        ----
        index : int
            ドロップダウンリスト上から何番目の要素を取得するか
            1:個人 2:グループ 3:個人宛以外
        '''
        self.select_index = index
        self.page_wait("paging-txt")
        dropdown = self.driver.find_element_by_xpath("//*[@id='informationType']")
        select = Select(dropdown)
        select.select_by_value(str(index))

    def get_time_list(self):
        '''お知らせ一覧の時間を返す関数

        Returns
        -------
        time_stamp_list : list[`datetime`]
            時間リスト(降順)
        '''
        self.page_wait("paging-txt")  # wait for page loading
        list_length = len(self.driver.find_elements_by_class_name("result-list"))  # get how many elements there are

        for i in range(1, list_length + 1):
            xpath = "//*[@id='information']/div/div[2]/div[{}]/div[2]/span[1]".format(
                i)
            time_stamp = self.driver.find_element_by_xpath(xpath)  # find xpath
            inner_text = time_stamp.text  # get text in tag
            inner_text_dt = datetime.datetime.strptime(
                inner_text, "%Y/%m/%d %H:%M")  # string to datetime
            self.time_stamp_list.append(inner_text_dt)  # add list

        return self.time_stamp_list

    def get_title_list(self):
        '''お知らせ一覧のタイトルを返す関数

        Returns
        -------
        title_list : list[`string`]
            タイトルリスト(降順)
        '''
        self.page_wait("paging-txt")  # wait for page loading
        list_length = len(
            self.driver.find_elements_by_class_name("result-list"))  # get how many elements there are

        for i in range(1, list_length + 1): #選択したものによってxpathの構造が変わっているので条件分岐
            if self.select_index == 2: # グループ
                xpath = "//*[@id='information']/div/div[2]/div[{}]/div[1]/span".format(
                    i)
            else: # 個人・個人宛以外
                xpath = "//*[@id='information']/div/div[2]/div[{}]/div[1]/span[2]".format(
                    i)

            title = self.driver.find_element_by_xpath(xpath)  # find xpath
            inner_text = title.text  # get text in tag
            self.title_list.append(inner_text)  # add list

        return self.title_list

    def close_browser(self):
        self.driver.quit()

    def count_message(self):
        '''1時間以内に投稿されたお知らせの数を返す処理
        
        Returns
        -------
        count_num : int
            1時間以内に投稿されたお知らせの数
        '''
        count_num = 0 # 初期カウント数
        cor_t = datetime.datetime.now() #現在時刻取得
        for i in range(len(self.time_stamp_list)):
            if  cor_t - datetime.timedelta(minutes=settings.INTERVAL_MINUTES) < self.time_stamp_list[i] :  #一時間前と大小比較
                count_num += 1

        return count_num 
