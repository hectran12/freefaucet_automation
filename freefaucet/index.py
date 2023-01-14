import json, time, base64, requests, sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
logs = []
count_logs = 0
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
def solveAntibotLinks (selfimage, listImage):
    jsonen = json.dumps({
        'self_image': selfimage,
        'image_list': str(base64.b64encode(json.dumps({
            "count_image": 4,
            "images": listImage
        }).encode())).replace("b'", '').replace("'", ''),
        'type_solve': '1'
    })
    encoded_string = str(base64.b64encode(jsonen.encode())).replace("b'", '').replace("'", '')
    data = {
    'type': 'antibotlinks',
    'data': encoded_string
    }
    solve = requests.post(url='https://tronghoa.dev/free-bypass-captcha/solve.php', data=data)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        return [True, json.loads(base64.b64decode(solve.json()["solution"]))]

def solveRecaptchav2GetTask ():
    data = json.dumps({
        'websiteURL': 'https://claimfreecoins.io/',
        'websiteKey': '',
        'isInvisible': 'false'
    }).encode()
    bs64 = str(base64.b64encode(data)).replace("b'", '').replace("'", '')
    url = 'https://tronghoa.dev/free-bypass-captcha/solve.php?type=recaptchav2&data={0}'.format(bs64)
    solve = requests.get(url)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        return [True, json.loads(base64.b64decode(solve.json()["taskId"]))]

def getConfig ():
    # read file config.json
    with open('config.json') as config:
        data = json.load(config)
        return data

def driver_create ():
    op = Options()
    # add extension
    op.add_extension("ads.crx")
    return webdriver.Chrome(options=op)

def driver_close (driver):
    driver.quit()

def resetTab (driver):
    child = driver.window_handles[0]
    driver.switch_to.window(child)

def closeTab (driver):
    driver.switch_to.window(driver.window_handles[1])
    driver.close()


def login (driver, wallet):
    
    if driver.page_source.find('Login') == -1:
        return False
    else:
        driver.find_element('name', 'address').send_keys(wallet)
        time.sleep(2)
        for x in range(2):
            try:
                driver.find_element('xpath', '//*[@id="faucet_form"]/div[3]/button').click()
                break
            except:
                time.sleep(1)
        time.sleep(2)
        if driver.page_source.find('Solve captcha then click on the AntiBot links in the following order to continue') == -1:
            return False 
        else:
            return True
def checkActive ():
    try:
        activeRq = requests.get('https://tronghoa.dev/free-bypass-captcha/active.php?mode=genLink').json()
        if activeRq['Status_Active'] == True:
            print(color.GREEN, 'You have activated the tool, please go to...')
            time.sleep(2)
            return True 
        else:
            print(color.BLUE, 'You have not activated the tool to use bypass, please activate via this link:')
            print(color.GREEN, activeRq['link'])
            return False
    except:
        return False
def solveRecaptchav2GetTask ():
    data = json.dumps({
        'websiteURL': 'https://freefaucet.link/',
        'websiteKey': '6LdcNAEhAAAAAIVEm1OUQ6qNor4hbx7F3kv5N6C7',
        'isInvisible': 'false'
    }).encode()
    bs64 = str(base64.b64encode(data)).replace("b'", '').replace("'", '')
    url = 'https://tronghoa.dev/free-bypass-captcha/solve.php?type=recaptchav2&data={0}'.format(bs64)
    solve = requests.get(url)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        resultJson = json.loads(base64.b64decode(solve.json()["response_anycaptcha"]))
        if resultJson['errorId'] == 0:
            return [True, resultJson['taskId']]


def getResponseRecaptchav2(taskId):
    data = json.dumps({
        'task_number': taskId
    }).encode()
    bs64 = str(base64.b64encode(data)).replace("b'", '').replace("'", '')
    url = 'https://tronghoa.dev/free-bypass-captcha/solve.php?type=recaptchav2&data={0}'.format(bs64)
    solve = requests.get(url)
    if solve.json()['error'] == True:
        return [False, solve.json()['message']]
    else:
        resultJson = json.loads(base64.b64decode(solve.json()["response_anycaptcha"]))
        return [True, resultJson]

def solveRecaptcha():
    taskId = solveRecaptchav2GetTask()
    if taskId[0] == True:
        taskId = taskId[1]
        status = False
        for x in range(25):
            response = getResponseRecaptchav2(taskId)
            if response[0] == True:
                response = response[1]
                if response['status'] == 'processing':
                    print(color.YELLOW, 'Solving recaptcha v2...')
                    status = False
                elif response['status'] == 'ready':
                    print(color.GREEN, 'successfully solved recaptcha v2')
                    solutionResponse = response['solution']['gRecaptchaResponse']
                    status = True
                    return solutionResponse
                else:
                    status = False
                    print(color.RED, 'Status does not exist, there is an error (recaptcha v2)')
            else:
                status = False
                print(color.RED, 'Retrieving response failed (recaptcha v2)')
            if status == False:
                time.sleep(5)
        print(color.RED, 'solution fail completely (recaptcha v2)')
        return False
    else:
        print(color.RED, 'Unable to get taskId')
        return False

def claim (driver):
    try:
        selfImage = driver.execute_script('var content = document.querySelector("#captchaModal > div > div > div.modal-header.alert.alert-info > div > img").src; return content;')
        selfImage = selfImage.replace('data:image/png;base64,','')
        className = driver.page_source.split('<a href="/" rel="')[0].split(' mr-auto')[1].split('"')[-1]

        img1 = driver.execute_script('var content = document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(1) > div.{0}.mr-auto.float-left.ml-4 > a > img").src; return content;'.format(
            className
        ))
        img1 = img1.replace('data:image/png;base64,','')
        img2 = driver.execute_script('var content = document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(1) > div.{0}.ml-auto.float-right.mr-4 > a > img").src; return content;'.format(
            className
        ))
        img2 = img2.replace('data:image/png;base64,','')
        img3 = driver.execute_script('var content = document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(4) > div.{0}.mr-auto.float-left.ml-4 > a > img").src; return content;'.format(
            className
        ))
        img3 = img3.replace('data:image/png;base64,','')
        img4 = driver.execute_script('var content = document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(4) > div.{0}.ml-auto.float-right.mr-4 > a > img").src; return content;'.format(
            className
        ))
        img4 = img4.replace('data:image/png;base64,','')
        imgs = [img1, img2, img3, img4]
        unique_list = []
        for element in imgs:
            if element not in unique_list:
                unique_list.append(element)
        if (len(imgs) != len(unique_list)):
            return False
        solveAnti = solveAntibotLinks(selfimage=selfImage, listImage=imgs)
        if solveAnti[0] == False:
            print(solveAnti[1])
            return False
        action = []
        
        for a in solveAnti[1]:
            if a == 1:
                action.append('document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(1) > div.{0}.mr-auto.float-left.ml-4 > a > img").click();'.format(
                    className
                ))
            elif a == 2:
                action.append('document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(1) > div.{0}.ml-auto.float-right.mr-4 > a > img").click();'.format(
                    className
                ))
            elif a == 3:
                action.append('document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(4) > div.{0}.mr-auto.float-left.ml-4 > a > img").click();'.format(
                    className
                ))
            elif a == 4:
                action.append('document.querySelector("#captchaModal > div > div > div.modal-body > div:nth-child(4) > div.{0}.ml-auto.float-right.mr-4 > a > img").click();'.format(
                    className
                ))
        if len(action) != len(set(action)) or len(action) < 4:
            return False
        for x in action:
            driver.execute_script(x)
            time.sleep(1)

        statusSolveRecaptcha = solveRecaptcha()
        if statusSolveRecaptcha == False:
            print(color.RED, 'Recaptcha failed')
            return False
        else:
            print(statusSolveRecaptcha)
            print(color.GREEN, 'successful recaptcha')
            driver.execute_script("document.getElementById('g-recaptcha-response').value = '{0}';".format(statusSolveRecaptcha))
            time.sleep(1)
            driver.find_element('name', 'login').click()
            time.sleep(3)
            if driver.page_source.find('was sent to your') == -1:
                
                return False
            else:
        
                return True
    except:
        return False
    


conf = getConfig()
wallet = conf['wallet']
ite = iter(wallet)
cols = color()
if checkActive() == False:
    input()
    sys.exit()
def resetIterConfig ():
    global ite
    ite = iter(wallet)


# get all wallet and print the screen
for x in ite:
    print(cols.GREEN + '[' + x + '] ' + cols.BLUE + ' = ' + cols.END + wallet[x])
resetIterConfig()

tags = {
    'btc' : '/free-bitcoin/?r=1Dotw12s2ed34wpXyh5gFwE29edbgemPpd',
    'doge' : '/free-dogecoin/?r=DJKntdmVqxZwJjBhRsZtsfaHmAAFbHAaEd',
    'ltc': '/free-litecoin/?r=MR4RsuJnNXWgfp9V6898VxZCzBLrVrz2MT',
    'trx': '/free-trxcoin/?r=TPw8AibYuVVXQUM6UcsvmyUaL6S4wAj6kL',
    'sql' : '/free-solanacoin/?r=D1MPLyFWEr4o4jzksF7gAu56KAx5gdtMnkEQPBNReY1o',
    'dash' : '/free-dash/?r=XrDoxcRinJkcrHhASdUkTJ8WuRrqMtBsyY'
}

drivers = driver_create()
time.sleep(3)
closeTab(drivers)
resetTab(drivers)

while True:
    for x in tags:
        for y in wallet:
            if x == y:
                while True:
                    try:
                        drivers.get('https://freefaucet.link' + tags[x])
                        log = login(drivers, wallet[y])
                        if log:
                            print(cols.GREEN + '[' + y + '] Login thanh cong')
                        elif log == None:
                            print(cols.RED + '[' + y + '] Chặn tính năng')
                            driver_close(drivers)
                            drivers = driver_create()
                            time.sleep(3)
                            closeTab(drivers)
                            resetTab(drivers)
                            break
                       
                        if claim(drivers) == False:
                            print(cols.RED + '[' + y + '] Claim that bai')
                            raise Exception('\rBYPASS Antibotlinks failed, proceeding to reset\r')
                        else:
                            print(cols.GREEN + '[' + y + '] Claim thanh cong')
                            break
                    except Exception as e:
                        print(e)
                        driver_close(drivers)
                        drivers = driver_create()
                        time.sleep(3)
                        closeTab(drivers)
                        resetTab(drivers)