# -*- coding: utf-8 -*-
import os, sqlite3  # 내장모듈
import pandas, numpy
import pcell, youtil  # xython 모듈
from pandas import pandas as pd
from xy_list import xy_list as xylist

class anydb:
	"""
	2024-09-08 : 전체적으로 손을 봄

	database를 사용하기 쉽게 만든것
	table, df의 자료는 [제일 첫컬럼에 컬럼이름을 넣는다]
	list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

	dblist_2d : series형태로된 리스트의 묶음, 일반 list_2d와는 가로세로가 반대로 되어있다
	"""

	def __init__(self, db_name=""):
		self.db_name = db_name
		self.util = youtil.youtil()

		self.sqlite_table_name = ""
		self.con = ""  # sqlite db에 연결되는 것

		if self.db_name != "":
			self.con = sqlite3.connect(db_name, isolation_level=None)
			self.cursor = self.con.cursor()

		self.check_db_for_sqlite(db_name)

	def append_df1_to_df2(self, input_df_1, input_df_2):
		"""
		dataframe자료의 뒤에 dataframe자료를 추가하는 것

		:param input_df_1:
		:param input_df_2:
		:return:
		"""
		result = pandas.concat([input_df_1, input_df_2])
		return result

	def change_anydata_to_dic(self, input_1, input_2=""):
		"""
		입력되는 자료를 사전형식으로 만드는 것
		입력형태 1 : [["컬럼이름1","컬럼이름2"],[["값1-1","값1-2"], ["값2-1","값2-2"]]]
		입력형태 2 : [[["컬럼이름1","값1"],["컬럼이름2","값2"]], [["컬럼이름1","값11"],["컬럼이름3","값22"]]]]
		입력형태 3 : ["컬럼이름1","컬럼이름2"],[["값1-1","값1-2"], ["값2-1","값2-2"]]

		:param input_1:
		:param input_2:
		:return: [{"컬럼이름1":"값1", "컬럼이름2": "값2"}, {"컬럼이름3":"값31", "컬럼이름2": "값33"}......]
		"""
		input_type = 0
		if input_2:
			input_type = 3
		else:
			if type(input_1[0][0]) == type([]):
				input_type = 2
			elif type(input_1[0][0]) != type([]) and type(input_1[1][0]) != type([]):
				input_type = 1

			result = []
			if input_type == 1:
				for value_list_1d in input_1[1]:
					one_line_dic = {}
					for index, column in enumerate(input_1[0]):
						one_line_dic[column] = value_list_1d[index]
					result.append(one_line_dic)
			elif input_type == 2:
				for value_list_2d in input_1:
					one_line_dic = {}
					for index, list_1d in enumerate(value_list_2d):
						one_line_dic[list_1d[0]] = list_1d[1]
					result.append(one_line_dic)
			elif input_type == 3:
				one_line_dic = {}
				for index, list_1d in enumerate(input_2):
					one_line_dic[input_1[index]] = list_1d[index]
				result.append(one_line_dic)
		return result

	def change_anyrange_to_xyxy(self, input_range=""):
		"""
		모든 :, ~ 의 스타일을 xyxy스타일로 바꾸는것
		기본은 0으로 시작한다
			elif "all" in input_value:
				result = "[:]"
		"""
		[x1, y1, x2, y2] = [0,0,0,0]
		if type(input_range) == type("abc"):
			if input_range =="all":
				pass
			elif "~" in input_range:
				if ":" in input_range:
					# 2 차원의 자료 요청건 ["2~3:4~5"]
					value1, value2 = input_range.split(":")
					if "~" in value2:
						start2, end2 = value2.split("~")
						if start2 == "" and end2 == "": #["2~3:~"]
							pass
						elif start2 == "" and end2:#["2~3:~5"]
							y2 = int(end2)
						elif start2 and end2 == "": #["2~3:4~"]
							x2 = int(start2)-1
						elif start2 and end2: #["2~3:4~5"]
							x2 = int(start2)-1
							y2 = int(end2)
						elif value2 == "":  # ["2~3:"]
							pass
						else:
							pass

					if "~" in value1:
						start1, end1 = value1.split("~")
						if start1 == "" and end1 == "": #["~:4~5"]
							pass
						elif start1 and end1 == "": #["2~:4~5"]
							x1 = int(start1)-1
						elif start1 == "" and end1: #["~3:4~5"]
							y1 = int(end1)
						elif start1 and end1: #["2~3:4~5"]
							x1 = int(start1)-1
							y1 = int(end1)
						elif value1 == "":  # [:"2~3"]
							pass
						else:
							pass
					else:
						pass

				else: #["1~2"], ~은 있으나 :이 없을때
					no1, no2 = input_range.split("~")
					if no1 and no2:
						if no1 == no2: #["1~1"]
							x1 = int(no1)-1
							y1 = int(no2)
						else :  # ["1~2"]
							x1 = int(no1)-1
							y1 = int(no2)
					elif no1 == "": #["~2"]
						y1 = int(no2)
					elif no2 == "": #["1~"]
						x1 = int(no1) - 1
					else: #["~"]
						pass

			elif ":" in input_range: # ~은 없고 :만 있을때
				no1, no2 = input_range.split(":")
				if no1 == "" and no2 == "": # [":"]
					pass
				elif no1 == "all":
					pass
				elif no1 == no2: # ["1:1"]
					x1 = int(no1)
					y1 = int(no2)
				elif no1 == "": # [":1"]
					y1 = int(no2)
				elif no2 == "": # ["1:"]
					x1 = int(no1)
				elif no2 == "all":
					pass
				else: # ["1:2"]
					x1 = int(no1)
					y1 = int(no2)

		return [x1, y1, x2, y2]

	def change_dblist_to_df(self, col_list="", dblist_2d=""):
		"""
		리스트 자료를 dataframe로 만드는것

		:param col_list: 제목리스트
		:param dblist_2d: 2차원 값리스트형
		:return: dataframe로 바꾼것
		"""
		checked_list_2d = self.util.change_list_1d_to_list_2d(dblist_2d)
		# 컬럼의 이름이 없거나하면 기본적인 이름을 만드는 것이다
		checked_col_list = self.check_input_data(col_list, dblist_2d)
		input_df = pandas.DataFrame(data=checked_list_2d, columns=checked_col_list)
		return input_df

	def change_dblist_to_df_rev1(self, dblist_2d, y_title_list="", x_title_list=""):
		"""
		2차원 리스트 자료를 dataframe형태로 만들어 주는것

		:param dblist_2d:
		:param y_title_list:
		:param x_title_list:
		:return:
		"""

		dic_l1d = self.change_dblist_to_dic_list_style(dblist_2d, y_title_list)
		if x_title_list == "":
			df_obj = pd.DataFrame(dic_l1d)
		else:
			df_obj = pd.DataFrame(dic_l1d, index = x_title_list)
		return df_obj

	def change_dblist_to_dic_list_style(self, dblist_2d, col_list=""):
		"""
		dataframe을 만드는 것은 기본으로 1차원의 series와 제목을 가진 사전형태의 자료를 자동으로 바꾼다

		:param dblist_2d:
		:param col_list:
		:return:
		"""
		temp = []
		result = {}
		if type(dblist_2d) == type([]):
			dblist_2d = self.util.check_list_2d(dblist_2d) #2차원이 아닐때 2차원으로 만들러 주는것
			dblist_2d = self.util.change_list_2d_to_same_max_len(dblist_2d) # 길이가 다를때 제일 긴것으로 똑같이 만들어 주는것
			#print("====> ", list_2d)
			# 별도로 column의 제목이 없다면, 1번부터 시작하는 번호를 넣어준다
			if col_list == "":
				for index, l1d in  enumerate(dblist_2d):
					temp.append(index+1)
				col_list = temp

			for index, l1d in enumerate(dblist_2d):
				result[col_list[index]] = dblist_2d[index]
		else:
			result = dblist_2d
		return result

	def change_df_to_dic(self, input_df, style="split"):
		"""
		dataframe자료를 사전형식으로 변경하는것
		dic의 형태중에서 여러가지중에 하나를 선택해야 한다

		입력형태 : data = {"calory": [123, 456, 789], "기간": [10, 40, 20]}
		출력형태 : dataframe
		dict :    {'제목1': {'가로제목1': 1, '가로제목2': 3}, '제목2': {'가로제목1': 2, '가로제목2': 4}}
		list :    {'제목1': [1, 2], '제목2': [3, 4]}
		series :  {열 : Series, 열 : Series}
		split :   {'index': ['가로제목1', '가로제목2'], 'columns': ['제목1', '제목2'], 'data': [[1, 2], [3, 4]]}
		records : [{'제목1': 1, '제목2': 2}, {'제목1': 3, '제목2': 4}]
		index :   {'가로제목1': {'제목1': 1, '제목2': 2}, '가로제목2': {'제목1': 3, '제목2': 4}}

		:param input_df:
		:param style:
		:return:

		"""
		checked_style = style
		if not style in ["split", "list", 'series', 'records', 'index']:
			checked_style = "split"
		result = input_df.to_dict(checked_style)
		return result

	def change_df_to_list(self, input_df):
		"""
		df자료를 커럼과 값을 기준으로 나누어서 결과를 리스트로 돌려주는 것이다

		:param input_df: dataframe객체
		:return: [[컬럼이름1, 컬럼이름2,,,,], [자료1], [자료2]....]
		"""
		col_list = input_df.columns.values.tolist()
		value_list = input_df.values.tolist()
		result = [col_list, value_list]
		return result

	def change_dic_to_list_as_col_n_value_style(self, input_dic):
		"""
		사전의 자료를 sql에 입력이 가능한 형식으로 만드는 것

		:param input_dic:
		:return: [[컬럼이름1, 컬럼이름2,,,,], [자료1], [자료2]....]
		"""
		col_list = list(input_dic[0].keys())
		value_list = []
		for one_col in col_list:
			value_list.append(input_dic[one_col])
		result = [col_list, value_list]
		return result

	def change_list_2d_to_dblist(self, list_2d):
		"""
		일반적인 list_2d와 df용 list_2d는 가로와 세로가 반대로 되어야 하기때문에
		dblist_2d로 해야 할것같다
		:param excel_2d:
		:return:
		"""
		list_2d = self.util.check_list_2d(list_2d)  # 2차원이 아닐때 2차원으로 만들러 주는것
		dblist_2d = self.util.change_xylist_to_yxlist(list_2d)
		return dblist_2d

	def change_list_2d_to_dblist_n_title(self, list_2d, first_is_title = True):
		"""
		2차원리스트를 제목과 dblist스타일의 자료로 만드는 것

		:param list_2d:
		:param first_is_title:
		:return:
		"""

		if first_is_title:
			title_list = list_2d[0]
			db_list_2d = self.util.change_xylist_to_yxlist(list_2d[1:])
		else:
			title_list = []
			db_list_2d = self.util.change_xylist_to_yxlist(list_2d)

		return [db_list_2d, title_list]

	def change_sqlite_table_name(self, table_name_old, table_name_new, db_name=""):
		"""
		현재 db에서 테이블 이름 변경

		:param sqlite_table_name_old:
		:param sqlite_table_name_new:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""

		self.check_db_for_sqlite(db_name)
		sql_sentence = "alter table %s rename to %s" % (table_name_old, table_name_new)
		self.cursor.execute(sql_sentence)

	def change_sqlite_table_to_df(self, sqlite_table_name, sqlite_db_name=""):
		"""
		sqlite의 테이블을 df로 변경

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		sql = "SELECT * From {}".format(sqlite_table_name)
		sql_result = self.cursor.execute(sql)
		cols = []
		for column in sql_result.description:
			cols.append(column[0])
		input_df = pandas.DataFrame.from_records(data=sql_result.fetchall(), columns=cols)
		return input_df

	def change_sqlite_table_to_list(self, sqlite_table_name, sqlite_db_name=""):
		"""
		sqlite의 테이블 자료를 리스트로 변경

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return: [2차원리스트(제목), 2차원리스트(값들)]
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		sql_result = self.cursor.execute("SELECT * From {}".format(sqlite_table_name))
		cols = []
		for column in sql_result.description:
			cols.append(column[0])
		temp = []
		for one in sql_result.fetchall():
			temp.append(list(one))
		result = [cols, temp]
		return result

	def check_basic_range(self, input_value):
		"""
		개인적으로 만든 이용형태를 것으로,
		check로 시작하는 메소드는 자료형태의 변경이나 맞는지를 확인하는 것이다
		dataframe의 영역을 나타내는 방법을 dataframe에 맞도록 변경하는 것이다
		x=["0:2"] ===> 1, 2열
		x=["1~2"] ===> 1, 2열
		x=["1,2,3,4"] ===> 1,2,3,4열
		x=[1,2,3,4]  ===> 1,2,3,4열
		x=""또는 "all" ===> 전부
		"""
		result = input_value
		if type(input_value) == type("abc"):
			if ":" in input_value:
				pass
			elif "~" in input_value:
				temp = input_value.split("~")
				result = "[" + str(int(temp[0])-1)+":" +temp[1]+ "]"
			elif "all" in input_value:
				result = "[:]"
			elif "" in input_value:
				result = "[:]"
			elif "," in input_value:
				changed_one = input_value.split(",")
				result = []
				for item in changed_one:
					result.append(int(item))
		return result

	def check_db_for_sqlite(self, sqlite_db_name=""):
		"""
		기본적으로 test_db.db를 만든다
		memory로 쓰면, sqlite3를 메모리에 넣도록 한다

		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		if sqlite_db_name == "" or sqlite_db_name == "memory":
			self.con = sqlite3.connect(":memory:")
		elif sqlite_db_name == "" or sqlite_db_name == "test":  # 데이터베이스를 넣으면 화일로 만든다
			sqlite_db_name = "test_db.db"
			self.con = sqlite3.connect(sqlite_db_name, isolation_level=None)
		else:
			self.con = sqlite3.connect(sqlite_db_name, isolation_level=None)
		self.cursor = self.con.cursor()

	def check_db_name_in_folder_for_sqlite(self, sqlite_db_name="", path="."):
		"""
		경로안에 sqlite의 database가 있는지 확인하는 것이다
		database는 파일의 형태이므로 폴더에서 화일이름들을 확인한다

		:param sqlite_db_name: 데이터베이스 이름
		:param path: 경로
		:return:
		"""
		db_name_all = self.util.get_all_file_name_in_folder(path)
		if sqlite_db_name in db_name_all:
			result = sqlite_db_name
		else:
			result = ""
		return result

	def check_df_range(self, input_range):
		"""
		df의 영역을 나타내는 방법을 df에 맞도록 변경하는 것이다
		"""
		result = []
		if type(input_range) == type("abc"):
			result = self.check_basic_range(input_range)
		if type(input_range) == type([]):
			for one_value in input_range:
				result.append(self.check_basic_range(one_value))
		return result

	def check_input_data(self, col_list, data_list):
		"""
		컬럼의 이름이 없으면, 'col+번호'로 컴럼이름을 만드는 것

		:param col_list: y컴럼의 이름들
		:param data_list:
		:return:
		"""
		result = []
		# 컬럼의 이름이 없거나하면 기본적인 이름을 만드는 것이다
		if col_list == "" or col_list == []:
			for num in range(len(data_list)):
				result.append("col" + str(num))
		else:
			result = col_list
		return result

	def check_range_in_df(self, input_value):
		result = self.check_basic_range(input_value)
		return result

	def check_title_name(self, temp_title):
		# 각 제목으로 들어가는 글자에 대해서 변경해야 하는것을 변경하는 것이다
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
		                ["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return temp_title

	def check_x_index_in_df(self, input_df, input_index):
		title_list = input_df.index
		result = None
		[ix1, iy1, ix2, iy2] = self.change_anyrange_to_xyxy(input_index)
		if ix1 == 0 and ix2 == 0:
			result = "'" + str(title_list[ix1]) + "':'" + str(title_list[- 1]) + ""
		else:
			result = "'" + str(title_list[ix1]) + "':'" + str(title_list[ix2]) + ""
		return result


	def check_x_index_in_df_old(self, input_df, input_index):
		"""
		index가 기본 index인 0부터 시작하는 것이 아닌 어떤 특정한 제목이 들어가 있는경우는
		숫자로 사용할수가 없다. 그래서 그서을 확인후에 기본 index가 아닌 경우는 제목으로 변경해 주는
		것을 할려고 한다
		"2~3"  ===>  '인천':'대구'

		:param input_df: dataframe객체
		:param input_index:
		:return:
		"""
		index_list = input_df.index
		two_data = False
		result = input_index
		if ":" == input_index or "all" == input_index or "" == input_index:
			result = ":"
		elif ":" in input_index:
			two_data = input_index.split(":")
		elif "~" in input_index:
			temp = input_index.split("~")
			two_data = [str(int(temp[0])-1),temp[1]]

		if two_data:
			if int(two_data[1]) >= len(index_list):
				result = "'" + str(index_list[int(two_data[0])]) + "':"
			else:
				result = "'" + str(index_list[int(two_data[0])]) + "':'" + str(index_list[int(two_data[1])-1]) + "'"
		return result

	def check_y_index_in_df(self, input_df, input_index):
		"""
		index가 기본 index인 0부터 시작하는 것이 아닌 어떤 특정한 제목이 들어가 있는경우는
		숫자로 사용할수가 없다. 그래서 그것을 확인후에 기본 index가 아닌경우는 제목으로 변경해 주는
		것을 할려고 한다
		"2~3"  ===>  '인천':'대구'

		:param input_df: dataframe객체
		:param input_index:
		:return:
		"""
		index_list = input_df.columns
		result = input_index
		two_data = False
		if ":" == input_index or "all" == input_index or "" == input_index:
			result = ":"
		elif ":" in input_index:
			two_data = input_index.split(":")
		elif "~" in input_index:
			temp = input_index.split("~")
			two_data = [str(int(temp[0]) - 1), temp[1]]
		if two_data:
			if type(int(two_data[0])) == type(1) and type(int(two_data[1])) == type(1):
				if int(two_data[1]) >= len(index_list):
					result = "'" + str(index_list[int(two_data[0])]) + "':"
				else:
					result = "'" + str(index_list[int(two_data[0])]) + "':'" + str(
						index_list[int(two_data[1])-1]) + "'"
		return result

	def check_ytitle(self, y_name):
		"""
		컬럼의 이름으로 쓰이는 것에 이상한 글자들이 들어가지 않도록 확인하는 것이다

		:param y_name: y 컬럼이름
		:return:
		"""
		for data1, data2 in [["'", ""], ["/", ""], ["\\", ""], [".", ""], [" ", "_"]]:
			y_name = y_name.replace(data1, data2)
		return y_name

	def connect_db_for_sqlite(self, sqlite_db_name=""):
		"""
		database에 연결하기

		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

	def delete_all_empty_y_in_df(self, input_df):
		"""
		dataframe의 빈열을 삭제
		제목이 있는 경우에만 해야 문제가 없을것이다
		"""
		nan_value = float("NaN")
		input_df.replace(0, nan_value, inplace=True)
		input_df.replace("", nan_value, inplace=True)
		input_df.dropna(how="all", axis=1, inplace=True)
		return input_df

	def delete_empty_y_in_df(self, input_df):
		result = self.delete_all_empty_y_in_df(input_df)
		return result


	def delete_empty_y_in_sqlite_table(self, sqlite_table_name, sqlite_db_name=""):
		"""
		테이블의 컬럼중에서 아무런 값도 없는 컬럼을 삭제한다

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		y_name_all = self.read_all_ytitle_list_in_sqlite_table(sqlite_table_name, sqlite_db_name)

		for y_name in y_name_all:
			sql = ("select COUNT(*) from %s where %s is not null" % (sqlite_table_name, y_name))
			self.cursor.execute(sql)
			if self.cursor.fetchall()[0][0] == 0:
				# 입력값이 없으면 0개이고, 그러면 삭제를 하는 것이다
				sql = ("ALTER TABLE %s DROP COLUMN %s " % (sqlite_table_name, y_name))
				self.cursor.execute(sql)

	def delete_sqlite_memory_db(self):
		"""
		memory db는 connection을 close시키면, db가 삭제된다

		:return:
		"""
		self.con.close()

	def delete_sqlite_table(self, sqlite_table_name, sqlite_db_name=""):
		"""
		입력형태 : 테이블이름

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		self.cursor.execute("DROP TABLE " + sqlite_table_name)

	def delete_y_in_list_db_by_index(self, input_list_db, input_index_list=[1, 2, 3]):
		"""
		index번호를 기준으로 y라인을 삭제하는것
		list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

		:param input_list_db:
		:param input_index_list:
		:return:
		"""
		# 맨뒤부터 삭제가 되어야 index가 유지 된다
		checked_input_index_list = input_index_list.reverse()

		for index in checked_input_index_list:
			# y열의 제목을 지우는것
			input_list_db[0].pop(index)

			# 각 항목의 값을 지우는것
			for num in range(len(input_list_db[1])):
				input_list_db[1][num].pop(index)
		return input_list_db

	def delete_y_in_list_db_by_index_list(self, input_list_db, input_index_list=[1, 2, 3]):
		"""
		index번호를 기준으로 y라인을 삭제하는것
		list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

		:param input_list_db:
		:param input_index_list:
		:return:
		"""
		# 맨뒤부터 삭제가 되어야 index가 유지 된다
		checked_input_index_list = input_index_list.reverse()

		for index in checked_input_index_list:
			# y열의 제목을 지우는것
			input_list_db[0].pop(index)

			# 각 항목의 값을 지우는것
			for num in range(len(input_list_db[1])):
				input_list_db[1][num].pop(index)
		return input_list_db

	def delete_y_in_list_db_by_ytitle_list(self, input_list_db, input_name_list=["y_name_1, y_name_2"]):
		"""
		y라인 이름을 기준으로 삭제하는것
		list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

		:param input_list_db:
		:param input_name_list:
		:return:
		"""

		title_dic = {}
		for index in range(len(input_list_db[0])):
			title_dic[input_list_db[0][index]] = index

		input_index_list = []

		for name in input_name_list:
			index = title_dic[name]
			input_index_list.append(index)

		# 맨뒤부터 삭제가 되어야 index가 유지 된다
		result = self.delete_y_in_list_db_by_index(input_list_db, input_index_list)
		return result

	def delete_y_in_sqlite_table_by_ytitle_list(self, sqlite_table_name, y_name_list, sqlite_db_name=""):
		"""
		컬럼 삭제
		입력형태 : ["col_1","col_2","col_3"]
		y_name : 컬럼이름

		:param sqlite_table_name: 테이블 이름
		:param y_name_list:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		if y_name_list:
			for y_name in y_name_list:
				sql = ("ALTER TABLE %s DROP COLUMN %s " % (sqlite_table_name, y_name))
				self.cursor.execute(sql)

	def get_all_db_name_in_path(self, path=".\\"):
		"""
		모든 database의 이름을 갖고온다
		모든이 붙은것은 맨뒤에 all을 붙인다

		:param path: 경로
		:return:
		"""
		result = []
		for fname in os.listdir(path):
			if fname[-3:] == ".db":
				result.append(fname)
		return result

	def get_all_ytitle_in_sqlite(self, sqlite_table_name, sqlite_db_name=""):
		"""
		해당하는 테이의 컬럼구조를 갖고온다
		입력형태 : 테이블이름
		출력형태 : 컬럼이름들

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		self.cursor.execute("PRAGMA table_info('%s')" % sqlite_table_name)
		sql_result = self.cursor.fetchall()
		result = []
		for one_list in sql_result:
			result.append(one_list[1])
		return result

	def get_property_for_y_all_in_table_for_sqlite(self, sqlite_table_name, sqlite_db_name=""):
		"""
		해당하는 테이블의 컬럼의 모든 구조를 갖고온다

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		self.cursor.execute("PRAGMA table_info('%s')" % sqlite_table_name)
		result = []
		for temp_2 in self.cursor.fetchall():
			result.append(temp_2)
		return result

	def get_ytitle_list_from_no1_to_no2_in_table_for_sqlite(self, sqlite_table_name, offset=0, row_count=100, sqlite_db_name=""):
		"""
		테이블의 자료중 원하는 갯수만 읽어오는 것

		:param sqlite_table_name: 테이블 이름
		:param offset:
		:param row_count:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		self.cursor.execute(("select * from %s LIMIT %s, %s;") % (sqlite_table_name, str(offset), str(row_count)))
		result = self.cursor.fetchall()
		return result

	def insert_y_in_dblist(self, input_dblist, input_y_name, input_yline_data):
		"""
		맨끝에, 리스트형태의 자료를 세로열을 하나 추가하는 것

		:param input_list_db:
		:param input_y_name: 세로열의 이름
		:param input_yline_data: 세로열을 위한 자료
		:return:
		"""
		input_dblist[0].append(input_y_name)
		input_dblist[1].append(input_yline_data)
		return input_dblist

	def insert_y_in_list_db_with_index_by_ytitle_list(self, input_list_db, input_y_name, input_yline_data, input_index):
		"""
		index번호 위치에, 리스트형태의 자료를 세로열을 하나 추가하는 것

		:param input_list_db:
		:param input_y_name:
		:param input_yline_data:
		:param input_index:
		:return:
		"""
		input_list_db[0].insert(input_index, input_y_name)
		input_list_db[1].insert(input_index, input_yline_data)
		return input_list_db

	def insert_y_in_sqlite_memory_db_by_ytitle_list(self, sqlite_table_name, col_data_list_s):
		"""
		memory db에 새로운 컬럼을 넣는다

		:param sqlite_table_name: 테이블 이름
		:param col_data_list_s:
		:return:
		"""

		# 기존의 테이블의 컬럼이름들을 갖고온다
		all_exist_y_name = self.read_all_ytitle_list_in_sqlite_table(sqlite_table_name)

		for one_list in col_data_list_s:
			if type(one_list) == type([]):
				y_name = self.check_ytitle(one_list[0])
				col_type = one_list[1]
			else:
				y_name = self.check_ytitle(one_list)
				col_type = "text"
			if not y_name in all_exist_y_name:
				self.cursor.execute("alter table %s add column '%s' '%s'" % (sqlite_table_name, y_name, col_type))

	def insert_y_in_sqlite_table_by_ytitle_list(self, sqlite_table_name, col_data_list_s, sqlite_db_name=""):
		"""
		(여러줄) 새로운 새로 컬럼을 만든다
		col_data_list_s : [["이름1","int"],["이름2","text"]]
		["이름2",""] => ["이름2","text"]
		1차원리스트가 오면, 전부 text로 만든다

		:param sqlite_table_name: 테이블 이름
		:param col_data_list_s:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		for one_list in col_data_list_s:
			if type(one_list) == type([]):
				y_name = self.check_ytitle(one_list[0])
				col_type = one_list[1]
			else:
				y_name = self.check_ytitle(one_list)
				col_type = "text"
			self.cursor.execute("alter table %s add column '%s' '%s'" % (sqlite_table_name, y_name, col_type))

	def insert_ytitle_in_df(self, input_df, input_data):
		"""
		여러가지 형식으로 값을 넣어도 컬럼을 추가하는 방법입니다
		input_df.rename(columns={0: 'TEST', 1: 'ODI', 2: 'T20'}, inplace=True)
		df = pandas.DataFrame(data, columns=list_1d)

		:param input_df: dataframe객체
		:param input_data:
		:return:
		"""
		checked_changed_data = input_data
		if type(input_data) == type({}):
			# {0: 'TEST', 1: 'ODI', 2: 'T20'}
			checked_changed_data = input_data
		elif type(input_data[0]) == type([]) and len(input_data) == 1:
			# 이자료를 [["기존", "바꿀이름"], ["b", "bb"], ["c", "cc"]]
			checked_changed_data = {}
			for one in input_data:
				checked_changed_data[one[0]] = one[1]
		elif type(input_data[0]) == type([]) and len(input_data) == 2:
			# 이자료를 [["기존1", "기존2", "기존3", "기존3"], ["바꿀이름1", "바꿀이름2", "바꿀이름3", "바꿀이름3"]]
			checked_changed_data = {}
			for index, one in enumerate(input_data):
				checked_changed_data[input_data[index]] = input_data[index]
		elif type(input_data[0]) != type([]) and type(input_data) == type([]):
			# 이자료를 ["바꿀이름1", "바꿀이름2", "바꿀이름3", "바꿀이름3"]
			checked_changed_data = {}
			for index, one in enumerate(input_data):
				checked_changed_data[index] = input_data[index]
		input_df.rename(columns=checked_changed_data, inplace=True)
		return input_df

	def insert_yy_in_sqlite_table(self, sqlite_table_name, col_data_list_s, sqlite_db_name=""):
		"""
		(여러줄) 새로운 새로 컬럼을 만든다
		col_data_list_s : [["이름1","int"],["이름2","text"]]
		["이름2",""] => ["이름2","text"]
		1차원리스트가 오면, 전부 text로 만든다

		:param sqlite_table_name: 테이블 이름
		:param col_data_list_s:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		for one_list in col_data_list_s:
			if type(one_list) == type([]):
				y_name = self.check_ytitle(one_list[0])
				col_type = one_list[1]
			else:
				y_name = self.check_ytitle(one_list)
				col_type = "text"
			self.cursor.execute("alter table %s add column '%s' '%s'" % (sqlite_table_name, y_name, col_type))

	def is_ytitle_list(self, input_list):
		"""
		입력으로 들어온 1 차원 리스트자료가 컬럼이름으로 사용되는것인지 아닌지 확인하는것

		:param input_list:
		:return:
		"""
		result = 1
		result_empty = 0
		result_date_int = 0
		for one_value in input_list:
			if one_value == None or one_value == "":
				result_empty = result_empty + 1
			if type(one_value) == type(1):
				result_date_int = result_date_int + 1
			if result_empty > 0 or result_date_int > 0:
				result = 0
		return result

	def make_cursor_for_sqlite_db(self, sqlite_db_name=""):
		"""
		커서를 만드는 것
		:param sqlite_db_name:
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

	def make_db_for_sqlite(self, sqlite_db_name=""):
		"""
		(새로운 db 만들기) 새로운 데이터베이스를 만든다
		sqlite_db_name이 이미 있으면 연결되고, 없으면 새로 만듦
		입력형태 : 이름

		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

	def make_df_by_basic_style(self, dic_list_1d,column_list, index_list):
		df_obj = pd.DataFrame(dic_list_1d, columns=column_list, index=index_list)
		return df_obj

	def make_memory_db_for_sqlite(self):
		"""
		(새로운 메모리 db만들기)
		self.cursor.execute("CREATE TABLE " + self.sqlite_table_name + " (auto_no integer primary key AUTOINCREMENT)")
		memory에 생성하는 것은 바로 connection 이 만들어 진다

		:return:
		"""
		self.check_db_for_sqlite(":memory:")

	def make_sql_text_for_insert_by_y_names(self, sqlite_table_name, col_list):
		"""
		(sql구문 만들기) 컬럼이름을 추가하기 위하여 sql구문 만들기

		:param sqlite_table_name: 테이블 이름
		:param col_list: y컬럼 이름들
		:return:
		"""
		sql_columns = self.util.change_list_1d_to_one_text_with_chainword(col_list, ", ")
		sql_values = "?," * len(col_list)
		result = "insert into %s (%s) values (%s)" % (sqlite_table_name, sql_columns, sql_values[:-1])
		return result

	def make_sql_text_for_new_column_by_column_name_list(self, sqlite_table_name, col_list):
		result = self.make_sql_text_for_insert_by_y_names(sqlite_table_name, col_list)
		return result

	def make_sql_text_from_dic_data(self, sqlite_table_name, input_dic):
		"""
		(sql구문 만들기) 사전형의 자료를 기준으로 sql구문 만들기

		:param sqlite_table_name: 테이블 이름
		:param input_dic: 사전형 자료
		:return:
		"""

		sql_columns = ""
		sql_values = ""
		for one_key in input_dic.keys():
			value = input_dic[one_key]
			sql_columns = sql_columns + str(one_key) + ", "
			if value == None:
				sql_values = sql_values + str(value) + ", "
			elif type(value) == type(123) or type(value) == type(123.4):
				sql_values = sql_values + str(value) + ", "
			else:
				sql_values = sql_values + "'" + str(value) + "', "
		result = "insert into %s (%s) values (%s)" % (sqlite_table_name, sql_columns[:-2], sql_values[:-2])
		return result

	def make_table_for_sqlite_memory_db(self, sqlite_table_name):
		"""
		(새로운 테이블 만들기) 메모리db에 새로운 테이블 만들기

		:param sqlite_table_name: 테이블 이름
		:return:
		"""
		self.cursor.execute("CREATE TABLE IF NOT EXISTS " + sqlite_table_name + "(number integer)")

		all_sqlite_table_name = []
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
		sql_results = self.cursor.fetchall()
		for one in sql_results:
			all_sqlite_table_name.append(one[0])
		#print("모든 테이블 이름 ==> ", all_sqlite_table_name)

	def make_table_in_db_for_sqlite(self, sqlite_table_name, sqlite_db_name=""):
		"""
		(새로운 테이블 만들기) database는 먼저 선택해야 한다
		새로운 테이블을 만든다
		입력형태 : 테이블이름

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		# 현재 db안의 테이블에 같은 이름이 없는지 확인 하는 것
		tables = []
		self.cursor.execute("select name from sqlite_master where type = 'table'; ")
		all_sqlite_table_name = self.cursor.fetchall()
		if not sqlite_table_name in all_sqlite_table_name:
			self.cursor.execute("CREATE TABLE " + sqlite_table_name + " (Item text)")

	def make_table_with_y_for_sqlite(self, sqlite_table_name, column_data_list, sqlite_db_name=""):
		"""
		(새로운 테이블 만들기) 어떤 형태의 자료가 입력이 되어도 테이블을 만드는 sql을 만드는 것이다
		입력형태 1 : 테이블이름, [['번호1',"text"], ['번호2',"text"],['번호3',"text"],['번호4',"text"]]
		입력형태 2 : 테이블이름, ['번호1','번호2','번호3','번호4']
		입력형태 3 : 테이블이름, [['번호1',"text"], '번호2','번호3','번호4']

		:param sqlite_table_name: 테이블 이름
		:param column_data_list:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		sql_1 = "CREATE TABLE IF NOT EXISTS {}".format(sqlite_table_name)
		sql_2 = sql_1 + " ("
		for one_list in column_data_list:
			if type(one_list) == type([]):
				if len(one_list) == 2:
					y_name = one_list[0]
					col_type = one_list[1]
				elif len(one_list) == 1:
					y_name = one_list[0]
					col_type = "text"
			elif type(one_list) == type("string"):
				y_name = one_list
				col_type = "text"
			sql_2 = sql_2 + "{} {}, ".format(y_name, col_type)
		sql_2 = sql_2[:-2] + ")"
		self.cursor.execute(sql_2)
		return sql_2

	def read_all_table_name_in_sqlite_db(self, sqlite_db_name=""):
		"""
		(모든 테이블 이름들) 해당하는 테이의 컬럼구조를 갖고온다
		입력형태 : 데이터베이스 이름
		출력형태 : 테이블이름들

		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
		result = []
		for temp_2 in self.cursor.fetchall():
			result.append(temp_2[0])
		return result

	def read_all_ytile_list_in_sqlite_memory_db(self, sqlite_table_name):
		"""
		(모든 컬럼 이름) 모든 컬럼의 이름을 갖고오는 것, 메모리 db

		:param sqlite_table_name: 테이블 이름
		:return:
		"""
		self.cursor.execute("PRAGMA table_info('%s')" % sqlite_table_name)
		sql_result = self.cursor.fetchall()
		result = []
		for one_list in sql_result:
			result.append(one_list[1])
		return result

	def read_all_ytitle_list_in_sqlite_table(self, sqlite_table_name):
		"""
		(모든 컬럼 이름) 기존의 테이블의 컬럼이름들을 갖고온다

		:param sqlite_table_name: 테이블 이름
		:return:
		"""
		self.cursor.execute("PRAGMA table_info('%s')" % sqlite_table_name)
		sql_result = self.cursor.fetchall()
		all_exist_y_name = []
		for one_list in sql_result:
			all_exist_y_name.append(one_list[1])
		return all_exist_y_name

	def read_value_in_df_by_name(self, input_df, x, y):
		"""
		(dataframe의 1개의 값 읽어오기)
		열이나 행의 이름으로 pandas의 dataframe의 일부를 불러오는 것이다
		이것은 리스트를 기본으로 사용한다
		list_x=["가"~"다"] ===> "가"~"다"열
		list_x=["가","나","다","4"] ===> 가,나,다, 4 열
		x=""또는 "all" ===> 전부

		:param input_df: dataframe객체
		:param x:
		:param y:
		:return:
		"""

		temp = []
		for one in [x, y]:
			if ":" in one[0]:
				changed_one = one[0]
			elif "~" in one[0]:
				ed_one = one[0].split("~")
				changed_one = "'" + str(int(ed_one[0])-1) + "'" + ":" + "'" + str(ed_one[1]) + "'"
			elif "all" in one[0]:
				changed_one = "[:]"
			else:
				changed_one = one
			temp.append(changed_one)
		# 이것중에 self를 사용하지 않으면 오류가 발생한다
		exec("self.result = input_df.loc[{}, {}]".format(temp[0], temp[1]))
		return self.result

	def read_value_in_df_by_no(self, input_df, x, y):
		"""
		숫자번호로 pandas의 dataframe의 일부를 불러오는 것
		단, 모든것을 문자로 넣어주어야 한다
		x=["1:2", "1~2"] ===> 1, 2열
		x=["1,2,3,4"] ===> 1,2,3,4열
		x=[1,2,3,4]  ===> 1,2,3,4열
		x=""또는 "all" ===> 전부
		"""

		x_list = self.check_df_range(x)
		y_list = self.check_df_range(y)
		exec("self.result = input_df.iloc[{}, {}]".format(x_list, y_list))
		return self.result

	def read_value_in_df_by_xx(self, input_df, x):
		"""
		x의 라인들을 읽어온다

		:param input_df: dataframe객체
		:param x:
		:return:
		"""

		x_list = self.check_x_index_in_df(input_df, x)
		exec("self.result = input_df.loc[{}, {}]".format(x_list, ":"))
		return self.result

	def read_value_in_df_by_xy(self, input_df, xy=[0, 0]):
		"""
		(dataframe의 1개의 값 읽어오기)
		위치를 기준으로 값을 읽어오는 것이다
		숫자를 넣으면 된다

		:param input_df: dataframe객체
		:param xy:
		:return:
		"""
		result = input_df.iat[int(xy[0]), int(xy[1])]
		return result

	def read_value_in_df_by_xyxy(self, input_df, xyxy):
		"""
		4각 영역의 번호위치의 값을 읽어오기

		:param input_df: dataframe객체
		:param xyxy:
		:return:
		"""

		x11, y11, x22, y22 = xyxy

		x1 = min(x11, x22)
		x2 = max(x11, x22)
		y1 = min(y11, y22)
		y2 = max(y11, y22)

		x = str(x1) + ":" + str(x2)
		if x == "0:0":    x = ":"
		y = str(y1) + ":" + str(y2)
		if y == "0:0":    y = ":"

		x_list = self.check_x_index_in_df(input_df, x)
		y_list = self.check_y_index_in_df(input_df, y)
		#print(x_list, y_list)
		exec("self.result = input_df.loc[{}, {}]".format(x_list, y_list))
		return self.result

	def read_value_in_df_by_yy(self, input_df, y):
		"""
		y의 라인들을 읽어온다

		:param input_df: dataframe객체
		:param y:
		:return:
		"""
		y_list = self.check_y_index_in_df(input_df, y)
		exec("self.result = input_df.loc[{}, {}]".format(":", y_list))
		return self.result

	def read_value_in_sqlite(self, sqlite_table_name, sqlite_db_name=""):
		"""
		(테이블의 모든 값) 테이블의 모든 자료를 읽어온다
		입력형태 : 테이블 이름

		:param sqlite_table_name: 테이블 이름
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		self.cursor.execute(("select * from {}").format(sqlite_table_name))
		result = self.cursor.fetchall()
		return result

	def read_value_in_sqlite_memory_db_by_xy(self, sqlite_table_name, x_no, y_no):
		"""
		(한개의 값)메모리db의 x번째, y번째의 값

		:param sqlite_table_name: 테이블 이름
		:param x_no:
		:param y_no:
		:return:
		"""
		sql = f"select * from {sqlite_table_name} where x = {x_no} and y = {y_no}"
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		return result

	def read_value_in_sqlite_memory_db_with_ytitle_by_xy(self, sqlite_table_name, x_no, y_no):
		"""
		(한개의 값) 메모리db의 x번째, y번째의 값과 컬럼이름

		:param sqlite_table_name: 테이블 이름
		:param x_no:
		:param y_no:
		:return:
		"""
		sql = f"select * from {sqlite_table_name} where x = {x_no} and y = {y_no}"
		self.cursor.execute(sql)
		result = {}
		names = [description[0] for description in self.cursor.description]
		rows = self.cursor.fetchall()
		if rows == []:
			result = {}
		else:
			for row in rows:
				for name, val in zip(names, row):
					result[name] = val
		return result

	def read_value_in_sqlite_memory_db_with_ytitle_by_xy_except_none_data(self, sqlite_table_name, x_no, y_no):
		"""
		메모리db의 x번째, y번째의 값과 컬럼이름, 단 None값은 제외한다

		:param sqlite_table_name: 테이블 이름
		:param x_no:
		:param y_no:
		:return:
		"""
		sql = f"select * from {sqlite_table_name} where x = {x_no} and y = {y_no}"
		self.cursor.execute(sql)
		result = {}
		names = [description[0] for description in self.cursor.description]
		rows = self.cursor.fetchall()
		for row in rows:
			for name, val in zip(names, row):
				if val != None:
					result[name] = val
		return result

	def read_value_in_sqlite_table_by_ytitle_list(self, y_name_s="", condition="all", sqlite_db_name=""):
		"""
		컬럼이름으로 테이블 값을 갖고오기, 문자는 컬럼이름으로, 숫자는 몇번째인것으로...

		:param y_name_s:
		:param condition:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		if y_name_s == "":
			sql_columns = "*"
		else:
			sql_columns = self.util.change_list_1d_to_one_text_with_chainword(y_name_s, ", ")

		if condition == "all":
			lim_no = 100
		else:
			lim_no = condition
		limit_text = "limit {}".format(lim_no)
		sql = "SELECT {} FROM {} ORDER BY auto_no {}".format(sql_columns, self.sqlite_table_name, limit_text)
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		return result

	def read_value_in_table_as_dic_style_for_sqlite(self, sqlite_table_name):
		"""
		(테이블의 모든 값) 사전형식으로 돌려줌

		:param sqlite_table_name: 테이블 이름
		:return:
		"""
		sql = f"select * from {sqlite_table_name}"
		self.cursor.execute(sql)
		names = [description[0] for description in self.cursor.description]

		result = []
		all_lines = self.cursor.fetchall()
		for one_line in all_lines:
			temp = {}
			for index, value in enumerate(one_line):
				temp[names[index]] = value
			result.append(temp)
		return result

	def read_value_in_table_as_dic_style_for_sqlite_except_none(self, sqlite_table_name):
		"""
		(테이블의 모든 값) 사전형식으로 돌려줌, 단 None값은 제외한다

		:param sqlite_table_name: 테이블 이름
		:return:
		"""
		sql = f"select * from {sqlite_table_name}"
		self.cursor.execute(sql)
		names = [description[0] for description in self.cursor.description]
		result = {}
		all_lines = self.cursor.fetchall()
		for one_line in all_lines:
			temp = {}
			for index, value in enumerate(one_line):
				if value:
					temp[names[index]] = value
			if temp["x"] in result.keys():
				result[temp["x"]][temp["y"]] = temp
			else:
				result[temp["x"]] = {}
				result[temp["x"]][temp["y"]] = temp
		return result

	def read_xtitle_in_df_by_index(self, input_df, x_no=""):
		"""
		컬럼의 x의 index를 읽어오는 것이다

		:param input_df: dataframe객체
		:param x_no:
		:return:
		"""
		result = input_df.index
		if x_no != "":
			result = result[x_no]
		return result

	def read_xxyy_line_in_df(self, input_df, x, y=""):
		"""
		숫자번호로 pandas의 dataframe의 일부를 불러오는 것
		단, 모든것을 문자로 넣어주어야 한다
		x=["1:2", "1~2"] ===> 1, 2열
		x=["1,2,3,4"] ===> 1,2,3,4열
		x=[1,2,3,4]  ===> 1,2,3,4열
		x=""또는 "all" ===> 전부

		:param input_df: dataframe객체
		:param x:
		:param y:
		:return:
		"""

		x_list = self.check_x_index_in_df(input_df, x)
		y_list = self.check_y_index_in_df(input_df, y)
		#print(x_list, y_list)
		exec("self.result = input_df.loc[{}, {}]".format(x_list, y_list))
		return self.result

	def read_ytitle_in_df_by_index(self, input_df, y_no=""):
		"""
		컬럼의 y의 컬럼 제목을 읽어오는 것이다

		:param input_df: dataframe객체
		:param y_no:
		:return:
		"""
		result = input_df.columns
		if y_no != "":
			result = result[y_no]
		return result

	def run_sql_for_sqlite(self, sql, sqlite_db_name=""):
		"""
		sqlite의 sql문을 실행하는 것이다
		fetchall는
		첫번째 : (1, '이름1', 1, '값1')
		두번째 : (2, '이름2', 2, '값2')

		:param sql:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.con.commit()
		return result

	def run_sql_for_sqlite_memory_db(self, sql):
		"""
		sql실행

		:param sql:
		:return:
		"""
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.con.commit()
		return result

	def save_sqlite_memory_db_to_disk_db(self, sqlite_db_name=""):
		"""
		memory에 저장된것을 화일로 저장하는것
		python 3.7부터는 backup이 가능

		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		db_disk = sqlite3.connect(sqlite_db_name)
		self.con.backup(db_disk)

	def set_database_for_sqlite(self, sqlite_db_name=""):
		"""
		db만들기

		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

	def write_df_to_excel(self, input_df, xy=[1, 1]):
		"""
		df자료를 커럼과 값을 기준으로 나누어서 결과를 돌려주는 것이다

		:param input_df:
		:param xy:
		:return:
		"""
		col_list = input_df.columns.values.tolist()
		value_list = input_df.values.tolist()
		excel = pcell.pcell()
		excel.write_list_1d_from_cell_as_yline("", xy, col_list)
		excel.write_value_in_range_as_speedy("", [xy[0] + 1, xy[1]], value_list)

	def write_df_to_sqlite(self, sqlite_table_name, input_df, sqlite_db_name=""):
		"""
		df자료를 sqlite에 새로운 테이블로 만들어서 넣는 것

		:param sqlite_table_name: 테이블 이름
		:param input_df:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		input_df.to_sql(sqlite_table_name, self.con)

	def write_dic_to_sqlite(self, sqlite_table_name, input_dic, sqlite_db_name=""):
		"""
		사전형식의 값을 sqlite에 입력하는 것

		:param sqlite_table_name: 테이블 이름
		:param input_dic:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)

		for one_col in list(input_dic[0].keys()):
			if not one_col in self.read_all_ytitle_list_in_sqlite_table(sqlite_table_name, sqlite_db_name):
				self.insert_yy_in_sqlite_table(sqlite_table_name, [one_col], sqlite_db_name)

		sql = self.make_sql_text_for_insert_by_y_names(sqlite_table_name, list(input_dic[0].keys()))
		value_list = []
		for one_dic in input_dic:
			value_list.append(list(one_dic.values()))
		self.cursor.executemany(sql, value_list)

	def write_list_1d_to_sqlite(self, sqlite_table_name, y_name_s, input_list_1d, sqlite_db_name=""):
		"""
		리스트의 형태로 넘어오는것중에 y이름과 값을 분리해서 얻는 것이다

		:param sqlite_table_name: 테이블 이름
		:param y_name_s:
		:param list_1d:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		sql = self.make_sql_text_for_insert_by_y_names(sqlite_table_name, y_name_s)
		self.cursor.executemany(sql, input_list_1d)

	def write_value_in_df_by_xy(self, df, xy, value):
		"""
		dataframe에 좌표로 값을 저장

		:param df: dataframe
		:param xy:
		:param value:
		:return:
		"""
		x_max = df.index.size
		y_max = df.columns.size
		if xy[1] > y_max:
			for no in range(y_max, xy[1]):
				df[len(df.columns)] = numpy.NaN
		if xy[0] > x_max:
			data_set = [(lambda x: numpy.NaN)(a) for a in range(len(df.columns))]
			for no in range(xy[0] - x_max):
				df.loc[len(df.index)] = data_set
		df.iat[int(xy[0]), int(xy[1])] = value

	def write_value_in_sqlite(self, sqlite_table_name, input_1, input_2=""):
		"""
		입력하고싶은 값을 sqlite에 저장하는것

		:param sqlite_table_name: 테이블 이름
		:param input_1:
		:param input_2:
		:return:
		"""
		list_1d_dic = self.change_anydata_to_dic(input_1, input_2)
		sql_columns = ""
		sql_values = ""
		for one_dic in list_1d_dic:
			for one_key in one_dic.keys():
				sql_columns = sql_columns + one_key + ", "
				sql_values = sql_values + one_dic[one_key] + ", "
			sql = "insert into %s(%s) values (%s)" % (sqlite_table_name, sql_columns[:-2], sql_values[:-2])
			self.cursor.execute(sql)
		self.con.commit()

	def write_value_to_sqlite(self, sqlite_table_name, y_name_s, col_value_s, sqlite_db_name=""):
		"""
		값쓰기

		:param sqlite_table_name: 테이블 이름
		:param y_name_s:
		:param col_value_s:
		:param sqlite_db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(sqlite_db_name)
		sql_columns = ""
		sql_values = ""
		for column_data in y_name_s:
			sql_columns = sql_columns + column_data + ", "
			sql_values = "?," * len(y_name_s)
		sql = "insert into %s(%s) values (%s)" % (sqlite_table_name, sql_columns[:-2], sql_values[:-1])
		if type(col_value_s[0]) == type([]):
			self.cursor.executemany(sql, col_value_s)
		else:
			self.cursor.execute(sql, col_value_s)
		self.con.commit()


	def split_list_2d_as_data_xtitle_ytile(self, list_2d, xtitle_len, ytitle_len):
		# 2줄이상의 제목이 들어갈수있을것같아, 2차원의 자료로 만들었다
		l2d = self.util.check_list_2d(list_2d)
		xtitle_l2d = []
		ytitle_l2d = []
		data_l2d = []

		for l1d in l2d[ytitle_len:]:
			data_l2d.append(l1d[xtitle_len:])

		if xtitle_len:
			for l1d in l2d[ytitle_len:]:
				xtitle_l2d.append(l1d[:xtitle_len])

		if ytitle_len:
			for no in range(len(list_2d[0]) - xtitle_len):
				ytitle_l2d.append([])
				for l1d in l2d[:ytitle_len]:
					for index, one in enumerate(l1d[xtitle_len:]):
						ytitle_l2d[index].append(one)
		return [data_l2d, xtitle_l2d, ytitle_l2d]




