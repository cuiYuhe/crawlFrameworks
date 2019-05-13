import subprocess
import getpass
import os
import pwd
import shutil

class GitUtil(object):

    @classmethod
    def yh_clone_url(cls, url):

        # 确定路径
        dst_path = cls._dst_path_of_clone(url)
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)

        os.mkdir(dst_path)

        # 执行shell
        cls._clone_url_to_dst_path(url, dst_path)
        output = os.popen("pwd")
        print (output.read())

    @classmethod
    def _clone_url_to_dst_path(cls, url, dst_path):
        """
        clone到目的路径
        :param url: 将要clone的仓库
        :param dst_path: 目的路径
        :return:
        """
        os.system("git clone " + url + " " + dst_path)


    @classmethod
    def _dst_path_of_clone(cls, url):
        # 确定路径, 得到框架名称
        last_path = os.path.split(url)[-1]
        framework_name = os.path.splitext(last_path)[0]

        home_path = pwd.getpwuid(os.getuid()).pw_dir
        dst_folder_path = os.path.join(home_path, 'Desktop/tmp_git')
        if os.path.exists(dst_folder_path):
            shutil.rmtree(dst_folder_path)
        os.mkdir(dst_folder_path)
        dst_path = os.path.join(dst_folder_path, framework_name)

        return dst_path

if __name__ == '__main__':
    url = 'https://github.com/WenchaoD/FSCalendar.git'
    GitUtil.yh_clone_url(url)