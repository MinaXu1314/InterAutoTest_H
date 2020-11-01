from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig
"""
1. 使用excel工具类，获取结果（list）
2. 根据"是否运行"列的内容进行判断
3. 保存要执行的结果，放到新的列表（获取要执行的测试用例）
"""
class Data:
    def __init__(self, testcase_file, sheet_name):
        # 使用excel工具类，获取结果
        # self.reader = ExcelReader("../data/testdata.xlsx", "美多商城接口测试")
        self.reader = ExcelReader(testcase_file, sheet_name)
        # print(reader.data())

    def get_run_data(self):
        """
        根据是否运行列==y，获取执行测试用例
        :return: 
        """
        # 根据"是否运行"列的内容进行判断
        run_list = list()  # 定义一个空列表
        for line in self.reader.data():
            if str(line[DataConfig().is_run]).lower() == "y":
                # print(line)
                # 保存结果到列表中
                run_list.append(line)
        # print(run_list)
        return run_list

    def get_case_list(self):
        """
        获取全部测试用例
        :return: 
        """
        # run_list = list()
        # for line in self.reader.data():
        #     run_list.append(line)
        run_list = [line for line in self.reader.data()]
        return run_list

    def get_case_pre(self, pre):
        # 获取前置测试用例
        # List判断，执行，获取  最终呢生成一个最终的我们需要前置条件执行的测试用例
        """
        根据前置条件：从全部测试用例中获取到需要执行的前置测试用例
        :param pre: 
        :return: 
        """
        run_list = self.get_case_list()
        for line in run_list:
            if pre in dict(line).values():
                return line
        return None