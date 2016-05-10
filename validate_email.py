#coding:utf-8
__author__  = "pSkpt"
__version__ = "0.0.1"
__email__   = "pskpt.developer@gmail.com"
__status__  = "development"

import sys, os, time, getopt
import requests, json
import threading

class mailGun(object):
    def __init__(self, mail_list='mail_list.txt', mail_list_validated='mail_list_validated.txt', force_start=False, t_count=10):
        self.lock                = threading.RLock()
        self.th                  = []
        self.control             = True
        self.s_time              = time.time()
        self.api_key             = 'pubkey-5ogiflzbnjrljiky49qxsiozqef5jxp7'

        if mail_list is not None:
            self.mail_list = mail_list
        else:
            self.mail_list = 'mail_list.txt'

        if mail_list_validated is not None:
            self.mail_list_validated = mail_list_validated
        else:
            self.mail_list_validated = 'mail_list_validated.txt'

        if force_start is not None:
            self.force_start = force_start
        else:
            self.force_start = False

        if t_count is not None:
            self.t_count = int(t_count)
        else:
            self.t_count = 10

        if not os.path.exists(self.mail_list):
            print('{} file not found.'.format(self.mail_list))
            return

        finfo = os.stat(self.mail_list)
        if finfo.st_size <= 0:
            print('{} file is empty.'.format(self.mail_list))
            return

        self.list = [line.strip() for line in open(self.mail_list)]

        if self.force_start:
            pass
        else:
            if os.path.exists(self.mail_list_validated):
                finfo = os.stat(self.mail_list_validated)
                if finfo.st_size > 0:
                    while(1):
                        decision = input('{} file will reset. Do you want continue? (Yes/No) : '.format(self.mail_list_validated))
                        if decision.lower() == 'n' or decision.lower() == 'no':
                            sys.exit()
                        elif decision.lower() == 'y' or decision.lower() == 'yes':
                            break
                        else:
                            print('Unknown Command!')


        self.file = open(self.mail_list_validated, 'w')
        try:
            self.start()
        except KeyboardInterrupt:
            self.close()

    def start(self):
        if self.control:
            for mail in self.list:
                while threading.active_count() > self.t_count: time.sleep(0.1)
                self.thread(mail)
                print('[-] Checking Mail... ({})'.format(mail))
            self.close()

    def thread(self, mail):
        my_th = threading.Thread(target=self.get_validate,args=[mail])
        my_th.start()
        self.th.append(my_th)


    def get_validate(self, mail):
        result =  requests.get("https://api.mailgun.net/v3/address/validate",
        auth=("api", self.api_key),
        params={"address": '{}'.format(mail)})
        #self.file.write('{}\n\n'.format(result.text))
        if result.status_code == 401:
            print('401 Unauthorized - No valid API key provided')
            return
        try:
            r_json = json.loads(result.text)
        except ValueError:
            print('JSON Error')
            return
        self.save(mail, r_json['is_valid'])

    def save(self, mail, is_valid):
        with self.lock:
            save_text = '{} | {}\n'.format(mail, str(is_valid))
            self.file.write(save_text)
            print(save_text)

    def close(self):
        self.control = False
        print('[!] Closing...')
        for i in self.th:
            i.join()
        self.file.close()
        print('Total Execute Time : {:.2f}'.format((time.time()-self.s_time)))


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"i:o:t:fh",["input=","output=", "thread-count=", "force", "help"])
    except getopt.GetoptError:
        print('{} -i <input Mail List File=mail_list.txt> -o <output Validated Mail List=mail_list_validated.txt> -f (force Start)'.format(os.path.basename(__file__)))
        print('{} --input <input Mail List File=mail_list.txt> --output <output Validated Mail List=mail_list_validated.txt> --force (force Start)'.format(os.path.basename(__file__)))
        sys.exit(2)

    mail_list = mail_list_validated = force_start = t_count = None
    for opt, arg in opts:
        if opt == '-h':
            print('{} -i <input Mail List File=mail_list.txt> -o <output Validated Mail List=mail_list_validated.txt> -f (force Start)'.format(os.path.basename(__file__)))
            print('{} --input <input Mail List File=mail_list.txt> --output <output Validated Mail List=mail_list_validated.txt> --force (force Start)'.format(os.path.basename(__file__)))
            sys.exit()
        elif opt in ("-i", "--input"):
            mail_list = arg
        elif opt in ("-o", "--output"):
            mail_list_validated = arg
        elif opt in ("-t", "--thread-count"):
            t_count = arg
        elif opt in ("-f", "--force"):
            force_start = True
    
    validater = mailGun(mail_list, mail_list_validated, force_start, t_count)

if __name__ == "__main__":
   main(sys.argv[1:])