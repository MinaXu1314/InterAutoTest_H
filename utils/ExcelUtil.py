import os
import xlrd
"""
目的：实现数据驱动  返回list
1. 验证文件是否存在，存在读取，不存在报错
2. 验证读取sheet方式，名称还是索引
3. 读取sheet内容
4. 结果返回
"""
class SheetTypeError(Exception):
    """自定异常类"""
    pass

class ExcelReader:
    def __init__(self, excel_file, sheet_by):
        # 验证文件是否存在
        if os.path.exists(excel_file):
            self.excel_file = excel_file
            self.sheet_by = sheet_by
            self._data = list()
        else:
            raise FileNotFoundError("文件不存在")
    # 验证读取sheet方式  名称 or 索引
    def data(self):
        if not self._data:
            workbook = xlrd.open_workbook(self.excel_file)
            # 根据sheet_by的值，来执行不同的读取方式
            if type(self.sheet_by) not in [str, int]:
                raise SheetTypeError("请输入Int or Str类型的参数")
            elif type(self.sheet_by) == int:
                sheet = workbook.sheet_by_index(self.sheet_by)
            elif type(self.sheet_by) == str:
                sheet = workbook.sheet_by_name(self.sheet_by)
            # 读取sheet内容  返回list  元素：字典  格式：[{"a":"a1", "b":"b1"}, {"a":"a2", "b": "b2"}]
            # 1.获取首行的信息
            title = sheet.row_values(0)
            # 2.遍历测试行，与首行组成dict，放在List
            for row in range(1, sheet.nrows):  # 循环读取，过滤首行，从1开始
                row_value = sheet.row_values(row)
                # 与首行组成字典  放在list
                self._data.append(dict(zip(title, row_value)))
        # 返回结果
        return self._data

if __name__ == '__main__':
    reader = ExcelReader("../data/testdata.xlsx", "美多商城接口测试")
    print(reader.data())
