'''
・https://www.elms.hokudai.ac.jp/portal/home/information/list の表示中のお知らせから，掲載期間の前半部分を取得．
・datetime型でリストを返す．
'''
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
from selenium.webdriver.common.keys import Keys


class ScrapeElms:
    '''ELMSのスクレイプに関わる処理をするクラス
        ・ログインやMoodleのお知らせ情報をスクレイプする
        ・すべてインスタンス変数とし，クラス変数はない

    Attributes:
        ID (string) : user id
        PASSWORD (string) : user password
        time_stamp_list (list) : お知らせ一覧の時間リスト(datetime)
        driver (webdriver) : Chrome driver，webのスクレイピング操作に用いる
    '''
    def __init__(self, ID, PASSWORD):
        # initalize
        self.ID = ID
        self.PASSWORD = PASSWORD
        self.time_stamp_list = []

        # start driver with headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                       options=options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), ) # start driver with gui mode

    def page_wait(self, class_name):
        '''ページのロードを待つ関数
        Args:
            class_name (string)
        '''
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            # WebDriverWait(self.driver,
            #               15).until(EC.presence_of_all_elements_located)
        except Exception as ex:
            print(ex)

    def login(self):
        '''ログイン処理をする関数'''

        self.driver.get(
            "https://www.elms.hokudai.ac.jp/portal/home/information/list")
        id_input = self.driver.find_element_by_xpath(
            "//input[@id='username_input']")
        id_input.send_keys(self.ID)
        password_input = self.driver.find_element_by_xpath(
            "//input[@id='password_input']")
        password_input.send_keys(self.PASSWORD)

        login_button = self.driver.find_element_by_xpath(
            "//input[@id='login_button']")
        self.page_wait("signin-button")
        login_button.send_keys(Keys.ENTER)  # push Enter
        # login_button.click() #なぜかチャットBOTの画像が押されてしまうのでEnterに変更

    def getTimeList(self):
        '''お知らせ一覧を取得する関数

        Returns:
            time_stamp_list (list) : お知らせ一覧の時間リスト/降順(datetime)

        '''
        self.page_wait("result_paging_btn")  # wait for page loading
        list_length = len(
            self.driver.find_elements_by_class_name(
                "result-list"))  # get how many elements there are

        print("################# list_length", list_length)
        for i in range(1, list_length + 1):
            xpath = "//*[@id='information']/div/div[2]/div[{}]/div[2]/span[1]".format(
                i)
            time_stamp = self.driver.find_element_by_xpath(xpath)  # find xpath
            inner_text = time_stamp.text  # get text in tag
            inner_text_dt = datetime.datetime.strptime(
                inner_text, "%Y/%m/%d %H:%M")  # string to datetime
            print(inner_text_dt)
            self.time_stamp_list.append(inner_text_dt)  # add list

        return self.time_stamp_list


if __name__ == "__main__":
    elms = ScrapeElms("{ユーザーID}", "{パスワード}")
    elms.login()
    times_list = elms.getTimeList()
    print("\n################ times_list", times_list)
