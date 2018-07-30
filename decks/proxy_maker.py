import time
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import requests
from bs4 import BeautifulSoup
import re
import os
import shutil
import random
from django.http import HttpResponse
from django import forms
from io import BytesIO
import zipfile


class CodeInputForm(forms.Form):
    deck_code = forms.CharField(max_length=20,
                                min_length=20,
                                label="デッキコード",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control mr-4',
                                           "type": "text",
                                           'placeholder': '例：c4c8Jx-8aVtOj-cYxcax'}))
    type = forms.ChoiceField(choices=(("pdf", "pdf"), ("zip", "zip")),
                             label="ファイルタイプ",
                             initial="pdf",
                             widget=forms.RadioSelect(
                                 attrs={'class': 'btn btn-primary',
                                        "type": "text",
                                        })
                             )


def dl_img_and_return_http_response(deck_code: str):
    code = deck_code
    file_name = deck_code

    # html = requests.get("https://www.pokemon-card.com/deck/deck.html?deckID=11F1Fw-VNG8m4-fk1bVF").content
    html = requests.get("https://www.pokemon-card.com/deck/deck.html?deckID=" + code).content

    soup = BeautifulSoup(html, "html.parser")

    card_data_script_text = soup.find_all("script")[-1].text

    # deck_pke_list の例: [["33525", "3"], ["33525", "3"]]
    deck_pke_list = [elem.split("_")[:2] for elem in soup.find(id="deck_pke")["value"].split("-")]
    deck_gds_list = [elem.split("_")[:2] for elem in soup.find(id="deck_gds")["value"].split("-")]\
        if soup.find(id="deck_gds")["value"] != "" else []
    deck_sup_list = [elem.split("_")[:2] for elem in soup.find(id="deck_sup")["value"].split("-")]\
        if soup.find(id="deck_sup")["value"] != "" else []
    deck_sta_list = [elem.split("_")[:2] for elem in soup.find(id="deck_sta")["value"].split("-")]\
        if soup.find(id="deck_sta")["value"] != "" else []
    deck_ene_list = [elem.split("_")[:2] for elem in soup.find(id="deck_ene")["value"].split("-")]\
        if soup.find(id="deck_ene")["value"] != "" else []
    deck_ajs_list = [elem.split("_")[:2] for elem in soup.find(id="deck_ajs")["value"].split("-")]\
        if soup.find(id="deck_ajs")["value"] != "" else []

    deck_list = deck_pke_list + deck_gds_list + deck_sup_list + deck_sta_list + deck_ene_list + deck_ajs_list
    cards_to_print_count = 0

    individual_print_card_list = []

    temp_dir_name = "_ProxyTempFiles_"
    try:
        os.mkdir(temp_dir_name)
    except FileExistsError:
        pass

    def download_image(img_url, out_path_and_name):
        data = requests.get(img_url).content
        with open(out_path_and_name, mode="wb") as f:
            f.write(data)

    dl_counter = 0
    total_dls = len(deck_list)

    for elm in deck_list:
        dl_counter += 1
        pattern = re.compile(r"]='(/assets/images/card_images/large/[^\n]+/0+%s_[^\n]+\.jpg)'" % elm[0],
                             re.MULTILINE | re.DOTALL)
        match = pattern.search(card_data_script_text)

        if match:
            url = "http://www.pokemon-card.com" + match.group(1)
            elm.append(url)
            img_file_name = url.split("/")[-1]
            elm.append(img_file_name)

            if os.path.exists("./" + temp_dir_name + "/" + img_file_name):
                pass
            else:
                # print("画像の保存中:", dl_counter, "/", total_dls)
                download_image(url, "./" + temp_dir_name + "/" + img_file_name)
    #    print(elm)
        else:
            # たまに画像がなくて裏面の画像なことがあるので、その対応
            url = "http://www.pokemon-card.com/assets/images/noimage/poke_ura.jpg"
            elm.append(url)
            img_file_name = url.split("/")[-1]
            elm.append(img_file_name)

            if os.path.exists("./" + temp_dir_name + "/" + img_file_name):
                pass

            print("画像なし: 代替画像の保存中:", dl_counter, "/", total_dls)
            download_image(url, "./" + temp_dir_name + "/" + img_file_name)

        for i in range(int(elm[1])):
            cards_to_print_count += 1
            individual_print_card_list.append("./" + temp_dir_name + "/" + elm[3])

    # httpレスポンスの作成
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + deck_code + '.pdf"'

    # キャンバスと出力ファイルの初期化
    pdf_made = canvas.Canvas(response)
    pdf_made.saveState()

    # A4サイズに設定(JIS規格の紙の大きさ。実際の印刷範囲は10mm四方短い190x277程度だと思われる)
    pdf_width = 210.0*mm
    pdf_height = 297.0*mm
    pdf_made.setPageSize((pdf_width, pdf_height))

    pdf_made.setAuthor('PTCG2win')
    pdf_made.setTitle(deck_code)
    pdf_made.setSubject("PDF to print")

    # ポケモンカードのサイズは63x88なので、紙を縦置きにした場合、3枚x3枚(189x264)入る。
    num_card = cards_to_print_count
    # print("Page 1")
    for i in range(num_card):
        # 9枚ごとに改ページ
        if i != 0 and i % 9 == 0:
            pdf_made.showPage()
    #        print("Page", i // 9 + 1)
        # 3枚ごとに改行
        x_pos = (11 + 63 * (i % 3)) * mm
        y_pos = (15 + 88 * ((i % 9) // 3)) * mm
        pdf_made.drawInlineImage(
                                  individual_print_card_list[i],
                                  x_pos,
                                  y_pos,
                                  width=63 * mm,
                                  height=88 * mm,
                                  )
    # print("PDF生成中...")
    pdf_made.save()

    # レスポンスを返す
    return response

    # 削除する場合は下のコメントアウトを外す。(キャッシュが効くので削除しないことを推奨)
    # shutil.rmtree("./" + temp_dir_name)

    # print("終了！")


def dl_img_and_return_zip_http_response(deck_code: str):
    code = deck_code
    if len(code) != 20:
        return HttpResponse("The code you put '" + code + "' is not a valid deck code.")

    file_name = deck_code

    # html = requests.get("https://www.pokemon-card.com/deck/deck.html?deckID=11F1Fw-VNG8m4-fk1bVF").content
    html = requests.get("https://www.pokemon-card.com/deck/deck.html?deckID=" + code).content

    soup = BeautifulSoup(html, "html.parser")

    card_data_script_text = soup.find_all("script")[-1].text

    # deck_pke_list の例: [["33525", "3"], ["33525", "3"]]
    deck_pke_list = [elem.split("_")[:2] for elem in soup.find(id="deck_pke")["value"].split("-")]
    deck_gds_list = [elem.split("_")[:2] for elem in soup.find(id="deck_gds")["value"].split("-")]\
        if soup.find(id="deck_gds")["value"] != "" else []
    deck_sup_list = [elem.split("_")[:2] for elem in soup.find(id="deck_sup")["value"].split("-")]\
        if soup.find(id="deck_sup")["value"] != "" else []
    deck_sta_list = [elem.split("_")[:2] for elem in soup.find(id="deck_sta")["value"].split("-")]\
        if soup.find(id="deck_sta")["value"] != "" else []
    deck_ene_list = [elem.split("_")[:2] for elem in soup.find(id="deck_ene")["value"].split("-")]\
        if soup.find(id="deck_ene")["value"] != "" else []
    deck_ajs_list = [elem.split("_")[:2] for elem in soup.find(id="deck_ajs")["value"].split("-")]\
        if soup.find(id="deck_ajs")["value"] != "" else []

    deck_list = deck_pke_list + deck_gds_list + deck_sup_list + deck_sta_list + deck_ene_list + deck_ajs_list
    cards_to_print_count = 0

    individual_print_card_list = []

    temp_dir_name = "_ProxyTempFiles_"
    try:
        os.mkdir(temp_dir_name)
    except FileExistsError:
        pass

    def download_image(img_url, out_path_and_name):
        data = requests.get(img_url).content
        with open(out_path_and_name, mode="wb") as f:
            f.write(data)

    dl_counter = 0
    total_dls = len(deck_list)

    for elm in deck_list:
        dl_counter += 1
        pattern = re.compile(r"]='(/assets/images/card_images/large/[^\n]+/0+%s_[^\n]+\.jpg)'" % elm[0],
                             re.MULTILINE | re.DOTALL)
        match = pattern.search(card_data_script_text)

        if match:
            url = "http://www.pokemon-card.com" + match.group(1)
            elm.append(url)
            img_file_name = url.split("/")[-1]
            elm.append(img_file_name)

            if os.path.exists("./" + temp_dir_name + "/" + img_file_name):
                pass
            else:
                # print("画像の保存中:", dl_counter, "/", total_dls)
                download_image(url, "./" + temp_dir_name + "/" + img_file_name)
    #    print(elm)
        else:
            # たまに画像がなくて裏面の画像なことがあるので、その対応
            url = "http://www.pokemon-card.com/assets/images/noimage/poke_ura.jpg"
            elm.append(url)
            img_file_name = url.split("/")[-1]
            elm.append(img_file_name)

            if os.path.exists("./" + temp_dir_name + "/" + img_file_name):
                pass

            print("画像なし: 代替画像の保存中:", dl_counter, "/", total_dls)
            download_image(url, "./" + temp_dir_name + "/" + img_file_name)

        for i in range(int(elm[1])):
            cards_to_print_count += 1
            individual_print_card_list.append("./" + temp_dir_name + "/" + elm[3])

    # httpレスポンスの作成
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="' + deck_code + '.zip"'

    # zipfileオブジェクト生成
    pdf_zip = zipfile.ZipFile(response, "w")

    # 1つ目のPDFファイル
    memory_file = BytesIO()

    # キャンバスと出力ファイルの初期化
    pdf_in_memory = canvas.Canvas(memory_file)
    pdf_in_memory.saveState()

    # A4サイズに設定(JIS規格の紙の大きさ。実際の印刷範囲は10mm四方短い190x277程度だと思われる)
    pdf_width = 210.0*mm
    pdf_height = 297.0*mm
    pdf_in_memory.setPageSize((pdf_width, pdf_height))

    # ポケモンカードのサイズは63x88なので、紙を縦置きにした場合、3枚x3枚(189x264)入る。
    num_card = cards_to_print_count
    # print("Page 1")
    for i in range(num_card):
        # 9枚ごとに改ページ
        if i != 0 and i % 9 == 0:
            # ページ終了処理
            pdf_in_memory.showPage()
            # PDF生成
            pdf_in_memory.save()
            # zipfile(response)に書き込み
            pdf_zip.writestr(deck_code + "_page" + str((i // 9)) + ".pdf", memory_file.getvalue())

            ##################################################

            # 新しいpdfを作成
            memory_file = BytesIO()

            # キャンバスと出力ファイルの初期化
            pdf_in_memory = canvas.Canvas(memory_file)
            pdf_in_memory.saveState()

            # A4サイズに設定(JIS規格の紙の大きさ。実際の印刷範囲は10mm四方短い190x277程度だと思われる)
            pdf_width = 210.0 * mm
            pdf_height = 297.0 * mm
            pdf_in_memory.setPageSize((pdf_width, pdf_height))

        #        print("Page", i // 9 + 1)
        # 3枚ごとに改行
        x_pos = (11 + 63 * (i % 3)) * mm
        y_pos = (15 + 88 * ((i % 9) // 3)) * mm
        pdf_in_memory.drawInlineImage(
                                  individual_print_card_list[i],
                                  x_pos,
                                  y_pos,
                                  width=63 * mm,
                                  height=88 * mm,
                                  )
    else:
        if i % 9 != 0:
        # ページ終了処理
            pdf_in_memory.showPage()
            # PDF生成
            pdf_in_memory.save()
            # zipfile(response)に書き込み
            pdf_zip.writestr(deck_code + "_page" + str((i // 9) + 1) + ".pdf", memory_file.getvalue())

    pdf_zip.close()

    # レスポンスを返す
    return response

    # 削除する場合は下のコメントアウトを外す。(キャッシュが効くので削除しないことを推奨)
    # shutil.rmtree("./" + temp_dir_name)

    # print("終了！")
