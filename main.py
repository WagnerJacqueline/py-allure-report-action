import os
import shutil
import subprocess
import logging


def main():
    workspace = os.path.sep + "github" + os.path.sep + "workspace"

    input_allure_results = os.environ["INPUT_ALLURE_RESULTS"]
    input_gh_pages = os.environ["INPUT_GH_PAGES"]
    input_github_run_num = os.environ["GITHUB_RUN_NUMBER"]
    input_github_run_id = os.environ["GITHUB_RUN_ID"]
    input_github_repo = os.environ["INPUT_GITHUB_REPO"]
    input_github_report_repo = os.environ["INPUT_GITHUB_REPORT_REPO"]

    path_allure_results = os.path.join(workspace, input_allure_results)
    path_gh_pages = os.path.join(workspace, input_gh_pages)

    mode = 0o777

    os.makedirs(path_allure_results, mode, exist_ok=True)
    os.makedirs(path_gh_pages, mode, exist_ok=True)

    subfolders_scanned = os.scandir(path_allure_results)

    gh_pages_url = "https://" + input_github_report_repo.split("/")[0] + ".github.io/" + \
                   input_github_report_repo.split("/")[1]

    for s in subfolders_scanned:
        report_sub_name = 'allure-report-' + s.name
        gh_pages_report_url = gh_pages_url + "/" + report_sub_name

        report_subfolder = os.path.join(path_gh_pages, report_sub_name)
        run_num_folder = os.path.join(report_subfolder, input_github_run_num)
        
        logging.debug(os.listdir(report_subfolder))

        index = open(report_subfolder + os.path.sep + "index.html", "w+")
        index.truncate(0)
        index.write(
            "<!DOCTYPE html><meta charset=\"utf-8\"><meta http-equiv=\"refresh\" content=\"0; URL=" + gh_pages_report_url + "/" + input_github_run_num + "/\">\r\n")
        index.write("<meta http-equiv=\"Pragma\" content=\"no-cache\"><meta http-equiv=\"Expires\" content=\"0\">")
        index.close()

        executor = open(path_allure_results + os.path.sep + s.name + os.path.sep + "executor.json", "w+")
        executor.truncate(0)
        executor.write(
            "{\"name\":\"GitHub Actions\",\"type\":\"github\",\"reportName\":\"Allure Report " + s.name + "\",\r\n")
        executor.write("\"url\":\"" + gh_pages_report_url + "\",\r\n")
        executor.write("\"reportUrl\":\"" + gh_pages_report_url + "/" + input_github_run_num + "/\",\r\n")
        executor.write(
            "\"buildUrl\":\"https://github.com/" + input_github_repo + "/actions/runs/" + input_github_run_id + "\",\r\n")
        executor.write(
            "\"buildName\":\"GitHub Actions Run #" + input_github_run_id + "\",\"buildOrder\":\"" + input_github_run_num + "\"}")
        executor.close()

        #environment = open(path_allure_results + os.path.sep + s.name + os.path.sep + "environment.properties", "w+")
        #environment.write("URL=" + gh_pages_report_url)
        #environment.close()

        os.makedirs(report_subfolder, mode, exist_ok=True)
        os.makedirs(run_num_folder, mode, exist_ok=True)

        shutil.copytree(report_subfolder + os.path.sep + "last-history",
                        path_allure_results + os.path.sep + s.name + os.path.sep + "history", dirs_exist_ok=True)

        allure_generate = subprocess.Popen(
            "allure generate --clean " + path_allure_results + os.path.sep + s.name + " -o " + run_num_folder,
            shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        allure_generate.wait()

        shutil.copytree(run_num_folder + os.path.sep + "history",
                        report_subfolder + os.path.sep + "last-history", dirs_exist_ok=True)


if __name__ == "__main__":
    main()
