import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *


class AdressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class MainApp(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KorallNet WebBrowser")
        self.CreateApp()
        self.setMinimumSize(800, 720)
        self.setWindowIcon(QIcon("img/logo.jpg"))

    def CreateApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.next_btn = QPushButton("")
        self.next_btn.clicked.connect(self.Go_Next)
        self.next_btn.setStatusTip('Следующая страница')
        self.tbar = QTabBar(movable=True, tabsClosable=True)
        self.tbar.tabCloseRequested.connect(self.CloseAnyTab)
        self.tbar.tabBarClicked.connect(self.ChangeTab)
        self.tbar.setCurrentIndex(0)
        self.tbar.setDrawBase(False)
        self.update_btn = QPushButton("⟳")
        self.update_btn.clicked.connect(self.updatepage)
        self.update_btn.setStatusTip('Обновить страничку')
        self.tabsnum = 0
        self.tabs = []
        self.toolbar = QWidget()
        self.toolbar.setObjectName("toolbar")
        self.toolbarlayout = QHBoxLayout()
        self.addrbar = AdressBar()
        self.newtab_btn = QPushButton('')
        self.addrbar.returnPressed.connect(self.Search)
        self.newtab_btn.clicked.connect(self.NewTab)
        self.newtab_btn.setStatusTip("Создать новую вкладку")
        self.back_btn = QPushButton("")
        self.back_btn.clicked.connect(self.Go_Back)
        self.back_btn.setStatusTip('Предыдущая страничка')
        self.toolbar.setLayout(self.toolbarlayout)
        self.toolbarlayout.addWidget(self.back_btn)
        self.toolbarlayout.addWidget(self.next_btn)
        self.toolbarlayout.addWidget(self.newtab_btn)
        self.toolbarlayout.addWidget(self.update_btn)
        self.toolbarlayout.addWidget(self.addrbar)
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)
        self.layout.addWidget(self.tbar)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.container)
        self.setLayout(self.layout)
        self.NewTab()
        self.show()

    def CloseAnyTab(self, i):
        self.tbar.removeTab(i)

    def NewTab(self):
        i = self.tabsnum
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)
        self.tabs[i].setObjectName("tab" + str(i))
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("https://ya.ru"))
        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.SetTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.SetTabContent(i, "url"))
        self.tabs[i].layout.addWidget(self.tabs[i].content)
        self.tabs[i].setLayout(self.tabs[i].layout)
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])
        self.tbar.addTab("Новая вкладка")
        self.tbar.setTabData(i, {"object": "tab" + str(i), "initial": i})
        self.tbar.setCurrentIndex(i)
        self.tabsnum += 1

    def SetAddBar(self, i):
        tab = self.tbar.tabData(i)["object"]
        if self.findChild(QWidget, tab).content == True:
            url = QUrl(self.findChild(QWidget, tab).content.url()).toString()
            self.AdressBar.setText(url)

    def ChangeTab(self, i):
        if self.tbar.tabData(i):
            tab = self.tbar.tabData(i)["object"]
            self.container.layout.setCurrentWidget(self.findChild(QWidget, tab))
            self.SetAddBar(i)

    def Search(self):
        txt = self.addrbar.text()
        i = self.tbar.currentIndex()
        tab = self.tbar.tabData(i)["object"]
        web_view = self.findChild(QWidget, tab).content
        if "http" in txt or "https" in txt:
            url = txt
        else:
            if "." not in txt:
                url = "https://yandex.ru/search/?text=" + txt
            else:
                url = "http://" + txt
        web_view.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        tab_name = self.tabs[i].objectName()
        c = 0
        is_working = True

        while is_working != False:
            tabdataname = self.tbar.tabData(c)
            if c >= 99:
                is_working = False
            if tab_name == tabdataname["object"]:
                if type == "title":
                    newtitle = self.findChild(QWidget, tab_name).content.title()
                    self.tbar.setTabText(c, newtitle)
                elif type == "icon":
                    newicon = self.findChild(QWidget, tab_name).content.icon()
                    self.tbar.setTabIcon(c, newicon)
                is_working = False
            else:
                c += 1

    def Go_Back(self):
        activeind = self.tbar.currentIndex()
        tb_name = self.tbar.tabData(activeind)["object"]
        tb_cont = self.findChild(QWidget, tb_name).content
        tb_cont.back()

    def Go_Next(self):
        activeind = self.tbar.currentIndex()
        tb_name = self.tbar.tabData(activeind)["object"]
        tb_cont = self.findChild(QWidget, tb_name).content
        tb_cont.forward()

    def updatepage(self):
        activeind = self.tbar.currentIndex()
        tb_name = self.tbar.tabData(activeind)["object"]
        tb_cont = self.findChild(QWidget, tb_name).content
        tb_cont.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)


    window = MainApp()

    with open("style.css", "r") as style:
        app.setStyleSheet(style.read())

    try:
        sys.exit(app.exec_())
    except:
        print("Exit")