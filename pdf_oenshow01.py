# streamlit run pdf_oenshow01.py

import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image
import datetime
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from contextlib import closing
import plotly.express as px
import base64
import qrcode
from pdf2image import convert_from_path
from reportlab.pdfbase.ttfonts import TTFont
import pytesseract
import os

from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# pdfmetrics.registerFont(TTFont('MSGothic', 'C:\\Windows\\Fonts\\MSGothic.ttc'))

# フォントを登録 KozMinPro Regular.otf MS Gothic
# pdfmetrics.registerFont(UnicodeCIDFont('KozMinPro-Regular', 'C:/Windows/Fonts/KozMinPro-Regular.otf'))
# pdfmetrics.registerFont(TTFont('KozMinPro-Regular', 'C:/Windows/Fonts/msgothic.ttc'))





# データベースに接続
db_name = './data/product30.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

menu = ["総合生産管理", "受注管理1", "出荷管理2", "在庫管理3", "注文管理4", "顧客管理5"]
submenu1 = ["受注1検索0", "受注1追加1", "受注1編集2", "受注1削除3"]
submenu2 = ["出荷2検索0", "出荷2追加1", "出荷2編集2", "出荷2削除3", "出荷2金額表示4"]
submenu3 = ["在庫3検索0", "在庫3追加1", "在庫3編集2", "在庫3削除3"]
submenu4 = ["注文4検索0_品番_注番", "注文4追加1_日付", '期間別請求書表示', 'invoice表示']
submenu5 = ["顧客5検索0", "顧客5追加1", "顧客5編集2", "顧客5削除3"]

# サイドバーにメニューを表示
choice = st.sidebar.selectbox("Menu", menu)


def show_invoice43():
    # title表示する
    st.title('月単位請求項目表示4')
    st.subheader('月単位請求を抽出します。')

    image = Image.open('./data/猪.png')
    st.image(image, width=70)

    # データベースに接続
    db_name = './data/product30.db'
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # 日付選択
    start_date = st.date_input("開始日を選択してください")
    end_date = st.date_input("終了日を選択してください")

    if st.button('実行'):
        # global qd_会社id
        # SQLクエリの作成と実行
        sql = """
            select t_出荷Data.品番, t_在庫Data.名称, t_在庫Data.単価, t_出荷Data.出荷数, t_出荷Data.出荷日, t_在庫Data.Tax, t_出荷Data.出荷金額
            FROM t_出荷Data INNER JOIN t_在庫Data
            ON t_出荷Data.品番 = t_在庫Data.品番
            WHERE t_出荷Data.出荷日 BETWEEN ? AND ?
        """
        c.execute(sql, (start_date.strftime('%Y/%m/%d'), end_date.strftime('%Y/%m/%d')))

        # 結果をデータフレームに変換して表示
        df = pd.DataFrame(c.fetchall(),
                          columns=['品番', '名称', '単価', '出荷数', '出荷日', 'Tax', '出荷金額'])
        st.write(df)

        # query_totalクエリを実行して、データフレームに変換
        query_total = f"SELECT sum(出荷金額) FROM t_出荷Data WHERE 出荷日 BETWEEN '" \
                      f"{start_date.strftime('%Y/%m/%d')}' AND '{end_date.strftime('%Y/%m/%d')}'"
        dd_出荷合計 = conn.execute(query_total).fetchone()[0]
        # st.write(f'出荷合計額: {dd_出荷合計:,}円')

        dd_請求金額 = int(dd_出荷合計) * 1.1
        dd_消費税額 = int(dd_出荷合計) * 0.1

        # カーソルを作成
        cursor = conn.cursor()

        # SQLクエリを実行して結果を取得
        query_count = f"SELECT COUNT(*) FROM t_出荷Data WHERE 出荷日 BETWEEN '" \
                      f"{start_date.strftime('%Y/%m/%d')}' AND '{end_date.strftime('%Y/%m/%d')}'"
        cursor.execute(query_count)
        result43 = cursor.fetchone()[0]
        st.write(result43)

        # データベースとの接続を閉じる
        conn.close()

        ###### Invoice帳票 And QRコードを作成 ######################################################################
        qr = qrcode.QRCode(
            version=10,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=2,
            border=8
        )

        # q_data = 'https://engineer-lifestyle-blog.com/'
        q_data = 'df'

        qr.add_data(q_data)
        qr.make()
        _img = qr.make_image(fill_color="black", back_color="#ffffff")
        _img.save('./data/qrcode45.png')
        img = Image.open('./data/qrcode45.png')
        img.show()

        ###### Invoice_issue を発行######################################################################
        # PDFファイルの保存先ディレクトリ "C:\Users\marom\Invoice"
        # pdf_directory = r"C:\Users\Invoice"
        pdf_directory = r"C:\Users\marom\Invoice"

        # 日付をYYYYMMDD形式に変換し、ファイル名に使用する
        today = date.today()
        today_str_cnv = today.strftime('%Y%m%d')

        # PDFファイルのパス
        pdf_path = f"{pdf_directory}\\Invoice_{today_str_cnv}.pdf"

        # PDFを作成する
        cv = canvas.Canvas(pdf_path, pagesize=portrait(A4))

        # 以下でPDFファイルを作成する処理を記述する

        # # PDFファイルを保存する
        # cv.save()
        #
        # # Streamlitにファイルの保存を通知する
        # st.write(f"PDF file saved at: {pdf_path}")

        # cv = canvas.Canvas('temp_format00.pdf', pagesize=portrait(A4))

        # # 日付をYYYYMMDD形式に変換し、ファイル名に使用する
        # today = date.today()
        # today_str_cnv = today.strftime('%Y%m%d')
        # cv = canvas.Canvas(f'Invoice_{today_str_cnv}.pdf', pagesize=portrait(A4))

        # # フォント登録
        # pdfmetrics.registerFont(UnicodeCIDFont('MSGothic'))

        # フォントサイズ定義
        # font_size1 = 20
        font_size2 = 14
        # フォント登録
        pdfmetrics.registerFont(TTFont('MSGothic', 'C:\\Windows\\Fonts\\MSGothic.ttc'))
        cv.setFont('MSGothic', font_size2)

        # 日付をYYYYMMDD形式に変換し、ファイル名に使用する
        # today = date.today()
        # today_str_cnv = today.strftime('%Y%m%d')
        # cv = canvas.Canvas(f'Invoice_{today_str_cnv}.pdf', pagesize=portrait(A4))

        # # フォント登録
        # pdfmetrics.registerFont(TTFont('MSGothic', 'C:\\Windows\\Fonts\\MSGothic.ttc'))

        # フォントサイズ定義
        font_size1 = 20
        font_size2 = 14
        font_size3 = 10
        # cv.setFont('HeiseiKakuGo-W5', font_size2)
        cv.setFont('MSGothic', font_size2)

        # 表題欄 (x座標, y座標, 文字)を指定
        # cv.setFont('HeiseiKakuGo-W5', font_size1)
        cv.setFont('MSGothic', font_size1)
        cv.drawString(50, 760, 'Invoice(期間別[月/日/任意]請求書)')

        # cv.setFont('HeiseiKakuGo-W5', font_size2)
        cv.setFont('MSGothic', font_size2)
        cv.drawString(450, 760, f'Inv- {today_str_cnv}')

        # 画像挿入(画像パス、始点x、始点y、幅、高さ) watermark.jpg
        cv.drawInlineImage('./data/com_logo01.png', 470, 670, 80, 80)
        cv.drawInlineImage('./data/qrcode45.png', 40, 25, 100, 100)

        # 顧客Dataより、[会社名][Email]][TEL][担当者]を抽出する
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        # query_totalクエリを実行して、データフレームに変換 qd_会社id
        # dd_会社ID = '1'
        # Comid_sql = conn.execute('SELECT * FROM t_顧客Data WHERE 会社ID = ?', (dd_会社ID,)).fetchall()
        qd_会社id = '1'
        Comid_sql = conn.execute('SELECT * FROM t_顧客Data WHERE 会社ID = ?', (qd_会社id,)).fetchall()

        # 顧客Dataの抽出
        dd_会社名 = Comid_sql[0][1]
        dd_Email = Comid_sql[0][2]
        dd_TEL = Comid_sql[0][5]
        dd_担当者 = Comid_sql[0][7]

        conn.commit()
        conn.close()

        # 見出し表題を記入する
        cv.drawString(50, 695, f'{dd_会社名} 御中　{dd_担当者}　様')
        cv.drawString(50, 680, dd_Email)
        cv.drawString(50, 665, dd_TEL)
        cv.drawString(430, 655, '（株）仁志田製作所')
        cv.drawString(405, 640, '東京都板橋区中台1-3-5')
        cv.drawString(385, 625, 'Supplier5678@gmail.com')
        cv.drawString(450, 610, '03(3111)1200')
        # cv.setFont('HeiseiKakuGo-W5', font_size2)
        cv.setFont('MSGothic', font_size2)

        # 期間の表材の作成
        string11 = f'{start_date} から{end_date}'
        cv.drawString(100, 570, f'{string11}納入分 請求金額:￥{int(dd_請求金額):,}円')

        cv.setLineWidth(1.5)
        # 線を描画(始点x、始点y、終点x、終点y)
        cv.line(95, 562, 520, 562)
        cv.line(45, 755, 560, 755)

        # cv.setFont('HeiseiKakuGo-W5', font_size3)
        cv.setFont('MSGothic', font_size3)

        # ヘッター欄
        cv.drawString(52, 534, '品  番')
        cv.drawString(132, 534, '名  称')
        cv.drawString(262, 534, '単  価')
        cv.drawString(312, 534, '出荷数')
        cv.drawString(367, 534, '出荷日')
        cv.drawString(447, 534, 'Tax')
        cv.drawString(492, 534, '出荷金額')

        # 一列目[品番]
        for i in range(len(df)):
            cv.drawString(42, 514 - (i * 20), str(df.iloc[i, 0]))

        # 二列目[名称]
        for i in range(len(df)):
            cv.drawString(122, 514 - (i * 20), str(df.iloc[i, 1]))

        # 三列目[単価]
        for i in range(len(df)):
            cv.drawString(252, 514 - (i * 20), "{:.2f}".format(df.iloc[i, 2]))

        # 四列目[出荷数]
        for i in range(len(df)):
            cv.drawString(307, 514 - (i * 20), "{:,}".format(df.iloc[i, 3]))

        # 五列目[出荷日]
        for i in range(len(df)):
            cv.drawString(357, 514 - (i * 20), str(df.iloc[i, 4]))

        # 六列目[Tax]
        for i in range(len(df)):
            cv.drawString(447, 514 - (i * 20), "{:,}".format(df.iloc[i, 5]))

        # 七列目[出荷金額]
        for i in range(len(df)):
            cv.drawString(477, 514 - (i * 20), "{:,}".format(df.iloc[i, 6]))

        # 表の作成[6列21行] # cv.showPage()  改行ページ
        cv.setLineWidth(1)
        xlist = (40, 120, 250, 300, 350, 440, 470, 575)  # 差分　80,160,80,80,100       6列21行
        ylist = (
            130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490,
            510, 530, 550)  # 差分　20(21行)
        cv.grid(xlist, ylist)

        # 小計額/消費税/合計額の表題
        cv.drawString(370, 104, '小計額')
        cv.drawString(340, 85, '消費税(10%)')
        cv.drawString(340, 65, '消費税( 8%)')
        cv.drawString(370, 45, '合計額')

        # 小計額/消費税/合計額のData
        cv.drawString(460, 105, f'￥{int(dd_出荷合計):,}円')
        cv.drawString(460, 85, f'￥{int(dd_消費税額):,}円')
        cv.drawString(460, 65, f'￥0円')
        cv.drawString(460, 45, f'￥{int(dd_請求金額):,}円')

        # 表の作成[1列4行]
        cv.setLineWidth(1)
        xlist = (410, 560)
        ylist = (40, 60, 80, 100, 120)
        cv.grid(xlist, ylist)

        # PDFファイルを保存
        cv.save()

        # Streamlitにファイルの保存を通知する
        st.write(f"PDF file saved at: {pdf_path}")


def invoice_show44():
    st.title('hello world')
    # PDFファイルのディレクトリパス "C:\Users\Invoice" "C:\Users\Invoice"
    pdf_directory = r"C:\Users\marom\Invoice"

    # PDFファイルの一覧を取得する
    pdf_files = os.listdir(pdf_directory)

    # PDFファイルを新しい順にソートする
    pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(pdf_directory, x)), reverse=True)

    # 選択ボックスにPDFファイルを表示する
    selected_pdf = st.selectbox("Select PDF", pdf_files)

    # PDFファイルのパス
    pdf_path = os.path.join(pdf_directory, selected_pdf)

    # PDFを画像に変換する
    images = convert_from_path(pdf_path)

    # 画像を表示する
    for i, image in enumerate(images):
        st.image(image, caption=f"Page {i + 1}")


# /////選択されたメニューに応じて、選択肢を表示////////////////////////////////////////////////////////////////////////
if choice == "受注管理1":
    # st.sidebar.markdown("Select a submenu:")
    submenu_choice = st.sidebar.selectbox("", submenu1)

    # 選択されたサブメニューの情報を表示
    if submenu_choice == "受注1検索0":
        findings10()
    elif submenu_choice == "受注1追加1":
        addings11()
    elif submenu_choice == "受注1編集2":
        changes12()
    elif submenu_choice == "受注1削除3":
        deletes13()

elif choice == "出荷管理2":
    st.sidebar.markdown("Select a submenu:")
    submenu_choice = st.sidebar.selectbox("", submenu2)

    # 選択されたサブメニューの情報を表示
    if submenu_choice == "出荷2検索0":
        findings20()
    elif submenu_choice == "出荷2追加1":
        addings21()
    elif submenu_choice == "出荷2編集2":
        changes22()
    elif submenu_choice == "出荷2削除3":
        deletes23()
    elif submenu_choice == "出荷2金額表示4":
        showamount24()

elif choice == "在庫管理3":
    st.sidebar.markdown("Select a submenu:")
    submenu_choice = st.sidebar.selectbox("", submenu3)

    # 選択されたサブメニューの情報を表示
    if submenu_choice == "在庫3検索0":
        finding30()
    elif submenu_choice == "在庫3追加1":
        adding31()
    elif submenu_choice == "在庫3編集2":
        changes32()
    elif submenu_choice == "在庫3削除3":
        delete33()

if choice == "注文管理4":
    st.sidebar.markdown("Select a submenu:")
    submenu_choice = st.sidebar.selectbox("", submenu4)

    # 選択されたサブメニューの情報を表示
    if submenu_choice == "注文4検索0_品番_注番":
        st.title('findings40()')
        # findings40()
    elif submenu_choice == "注文4追加1_日付":
        st.title('addings41()')
        # addings41()
    elif submenu_choice == "受注データ表示":
        st.title('show_data42()')
        # show_data42()
    elif submenu_choice == "期間別請求書表示":
        show_invoice43()
    elif submenu_choice == "invoice表示":
        invoice_show44()

elif choice == "顧客管理5":
    st.sidebar.markdown("Select a submenu:")
    submenu_choice = st.sidebar.selectbox("", submenu5)

    # 選択されたサブメニューの情報を表示
    if submenu_choice == "顧客5検索0":
        findings50()
    elif submenu_choice == "顧客5追加1":
        addings51()
    elif submenu_choice == "顧客5編集2":
        changes52()
    elif submenu_choice == "顧客5削除3":
        deletes53()


if choice == "総合生産管理":
    # global qd_会社id

    # title‘画像を表示する
    # st.title("総合生産管理(販売/生産に適用)")
    #
    # # SQLite3 DBに接続する
    # conn = sqlite3.connect(db_name)
    # c = conn.cursor()
    #
    # # 会社名のリストを取得する
    # c.execute('SELECT 会社名 FROM t_顧客Data')
    # company_names = [row[0] for row in c.fetchall()]
    #
    # # ユーザーに会社名を選択させる
    # selected_company_name = st.selectbox('Select a company name:', company_names)
    #
    # selected_company_index = company_names.index(selected_company_name)
    # qd_会社id = selected_company_index + 1
    # st.write(qd_会社id)

    # 選択された会社名を表示する
    # st.write('You selected:', selected_company_name)

    # title‘画像を表示する
    st.caption("受注管理1:")
    image = Image.open('./data/猫.png')
    st.image(image, width=70)

    st.caption("出荷管理2:")
    image1 = Image.open('./data/牛.png')
    st.image(image1, width=70)

    st.caption("在庫管理3:")
    image1 = Image.open('./data/犬.png')
    st.image(image1, width=70)

    st.caption("注文管理4:")
    image1 = Image.open('./data/猪.png')
    st.image(image1, width=70)

    st.caption("顧客管理5:")
    image1 = Image.open('./data/狐.png')
    st.image(image1, width=70)

# streamlit run pdf_oenshow01.py
