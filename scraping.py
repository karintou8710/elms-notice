'''
・ELMSのスクレイピングに関する処理を行う．
・以下メソッド
    ・getTimeList() -> タイムスタンプ一覧を返す
    ・getTitleList() -> タイトル一覧を返す
    ・login() -> ELMSログイン処理を行う
    ・page_wait() -> ページのロードを待つ
'''
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.common.keys import Keys


class ScrapeElms:
    '''ELMSのスクレイピングに関わる処理をするクラス
        ・ログインやMoodleのお知らせ情報をスクレイプする
        ・https://www.elms.hokudai.ac.jp/portal/home/information/list より．

    Params:
        ID : user id (string)
        PASSWORD : user password (string)
        time_stamp_list : タイムスタンプリスト(list[datetime])
        title_list : タイトルリスト (list[string])
        driver : Chrome driver(webdriver)，スクレイピング操作に用いるドライバ
    Args:
        ID(string)
        PASSWORD(string)
    '''
    def __init__(self, ID, PASSWORD):
        # initialization
        self.ID = ID
        self.PASSWORD = PASSWORD
        self.time_stamp_list = []
        self.title_list = []

        # start up driver with headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                       options=options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), ) # start driver with gui mode

    def page_wait(self, class_name):
        '''ページのロードを待つ関数
        driver.get()の後呼び出す．
        引数にクラス要素名を指定する必要あり．

        Args:
            class_name (string)
        '''
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            # WebDriverWait(self.driver,
            #               15).until(EC.presence_of_all_elements_located) #これだと上手くロード待機できなかった
        except Exception as ex:
            print(ex)

    def login(self):
        '''ログイン処理をする関数'''

        self.driver.get(
            "https://www.elms.hokudai.ac.jp/portal/home/information/list")
        self.page_wait("signin-button")  # wait for page loading

        id_input = self.driver.find_element(By.XPATH,
                                            "//input[@id='username_input']")
        id_input.send_keys(self.ID)
        password_input = self.driver.find_element(
            By.XPATH, "//input[@id='password_input']")
        password_input.send_keys(self.PASSWORD)

        login_button = self.driver.find_element(By.XPATH,
                                                "//input[@id='login_button']")
        self.page_wait("signin-button")
        login_button.send_keys(Keys.ENTER)  # push Enter
        # login_button.click() #なぜかチャットBOTの画像が押されてしまうのでEnterに変更

    def getTimeList(self):
        '''お知らせ一覧の時間を返す関数

        Returns:
            time_stamp_list : 時間リスト(降順)(list[datetime])
        '''
        self.page_wait("result_paging_btn")  # wait for page loading
        list_length = len(
            self.driver.find_elements(
                By.CLASS_NAME,
                "result-list"))  # get how many elements there are

        for i in range(1, list_length + 1):
            xpath = "//*[@id='information']/div/div[2]/div[{}]/div[2]/span[1]".format(
                i)
            time_stamp = self.driver.find_element(By.XPATH,
                                                  xpath)  # find xpath
            inner_text = time_stamp.text  # get text in tag
            inner_text_dt = datetime.datetime.strptime(
                inner_text, "%Y/%m/%d %H:%M")  # string to datetime
            # print(inner_text_dt)
            self.time_stamp_list.append(inner_text_dt)  # add list

        return self.time_stamp_list

    def getTitleList(self):
        '''お知らせ一覧のタイトルを返す関数

        Returns:
            title_list : タイトルリスト(降順)(list[string])
        '''
        self.page_wait("result_paging_btn")  # wait for page loading
        list_length = len(
            self.driver.find_elements(
                By.CLASS_NAME,
                "result-list"))  # get how many elements there are

        for i in range(1, list_length + 1):
            xpath = "//*[@id='information']/div/div[2]/div[{}]/div[1]/span[2]".format(
                i)
            title = self.driver.find_element(By.XPATH, xpath)  # find xpath
            inner_text = title.text  # get text in tag
            # print(inner_text)
            self.title_list.append(inner_text)  # add list

        return self.title_list


if __name__ == "__main__":
    elms = ScrapeElms("{ユーザーID}", "{パスワード}")
    elms.login()
    times_list = elms.getTimeList()
    print("\n############ 時間一覧 ############\n times_list", times_list)
    t_list = elms.getTitleList()
    print("\n############ タイトル一覧 ############\n title_list", t_list)
