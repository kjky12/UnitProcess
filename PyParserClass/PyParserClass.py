
import os
import csv

# HTML 문서의 데이터를 가져오기 위해 import
from bs4 import BeautifulSoup

def search(dirname, extfind, includeFileName, exceptFileName):
    lstFilePath = []
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == extfind:

                    if full_filename.find(includeFileName) >= 0 :
                        if includeFileName.find(exceptFileName) == -1 :
                            lstFilePath.append(full_filename)


                    #print(full_filename)
    except PermissionError:
        pass

    return lstFilePath




def ConvertHtmlToExcel(strHtmlPath, strSavePath) : 

    page = open(strHtmlPath, 'rt', encoding='utf-8').read() # HTML 파일 읽고 문자열 리턴
    soup = BeautifulSoup(page, 'html.parser')  # Soup 객체 생성
    
    
    header = soup.find(class_='headertitle')

    if(header.text.find("클래스 참조") < 0) :
        return;

    strHeader = header.text.replace(" 클래스 참조","")
    astrPath = strHeader.split('.')

    strMakeDirectory =''
    if len(astrPath) > 1 : # 디렉토리를 생성해야함
        for a in range(0 , len(astrPath) - 1) :
            strMakeDirectory += "\\" + astrPath[a]

        os.makedirs(strSavePath + "\\" + strMakeDirectory, exist_ok=True)

    #astrPath[len(astrPath) - 1]
    #if strHeader.find('.') > 0 :
    #    strMakePath = strHeader.replace('.','\\')
    #    os.mkdir(strSavePath + "\\" + strMakePath)
    #else :

    #csv생성
    strHeaderPath = strHeader.replace('.','\\')
    f = open(strSavePath + '\\' + strHeaderPath + '.csv', 'w', encoding='utf-16', newline='')
    wr = csv.writer(f)

    print("Start\t" + strHeaderPath)


    # Soup 객체를 이용하여 문서를 출력
    #print(soup.prettify())
    
    
    
    # HTML 문서 내부에 있는 <p>태그를 모두 검색
    #print(soup.find_all('td'))
    #print(soup.find_all(class_='memberdecls'))
    
    #전체 정보
    #for tag in soup.find_all(class_='memberdecls') :
    #    print(tag.get_text())
    
    
    #for tag in soup.find(class_='memberdecls') :
    #    tag.Trim()
    #    print(tag.get_text())
    
    
    #이게 좌측꺼 쭉 읽어오는거
    #for tag in soup.find_all(class_='memItemRight') :
    #    print(tag.get_text())
    
    
    for tagGroup in soup.find_all(class_='memberdecls') :
        #print(tagGroup)
    
        #tagDetail = tagGroup.find('memItemRight')
    
        for tagDetail in tagGroup.find_all('tr') :
            strText = str(tagDetail)        
    
            if strText.find('separator') > 0 :
                continue
    
            if strText.find('memdesc') > 0 :
                continue
            
            if strText.find('상속') > 0 :
                break
            
            strText2 = tagDetail.text

            
            strText2 = strText2.replace('static', '')
            strText2 = strText2.replace('virtual', '')
            strText2 = strText2.replace('override', '')
            strText2 = strText2.replace('\n', '')
            strText2 = strText2.replace('\xa0', ' ')
            strText2 = strText2.replace('[getset]', ' ')
            strText2 = strText2.replace('[set]', ' ')
            strText2 = strText2.replace('[get]', ' ')
            strText2 = strText2.replace('(', '(')
            strText2 = strText2.replace(')', ')')

            strText2 = strText2.strip()

            
            f.write(strText2+"\n")

            #wr.writerow([strText2])

            #초기화를 없앤다.
            #nFind = strText2.find('=')
            #if nFind > 0 :
            #    strText2 = strText2.substring(0, nFind)

            #print(tagDetail.get_text())
            #print(tagDetail.get_text())
    
    
        #for tagDetail in tagGroup.find_all(class_='memItemRight') :


    f.close()


lstFilPath = search('D:\\#Prodoc\\국통사\\클래스설계서_참고사항\\test\\PyParserClass\\PyParserClass\\html\\', '.html', 'class', 'members')


for filePath in lstFilPath :

    ConvertHtmlToExcel(filePath , os.getcwd() + "\\test")


print ("FINISH")